from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.workflow_exercises import (
    CASES, HARNESS, check, fingerprint, manifest_path, normalized, prepare, project_files,
)


PRICING_SOLUTION = '''
def price_line(unit_cents, quantity, discount_percent=0):
    if any(type(value) is not int for value in (unit_cents, quantity, discount_percent)):
        raise ValueError("integer inputs required")
    if unit_cents < 0 or quantity < 0 or not 0 <= discount_percent <= 100:
        raise ValueError("input out of range")
    return (unit_cents * quantity * (100 - discount_percent) + 50) // 100
'''

INVENTORY_SOLUTION = '''
def allocate(stock, requests):
    remaining = dict(stock)
    if any(type(count) is not int or count < 0 for count in stock.values()):
        raise ValueError("invalid stock")
    fulfilled = []
    for request in requests:
        quantity = request["quantity"]
        if type(quantity) is not int or quantity < 0:
            raise ValueError("invalid quantity")
        sku = request["sku"]
        count = min(remaining.get(sku, 0), quantity)
        fulfilled.append(count)
        if sku in remaining:
            remaining[sku] -= count
    return {"fulfilled": fulfilled, "remaining": remaining}
'''

REPORT_SOLUTION = '''
import json
import sys
from pathlib import Path
from pricing import price_line
from inventory import allocate

data = json.loads(Path(sys.argv[1]).read_text())
result = allocate(data["stock"], data["lines"])
result["total_cents"] = sum(price_line(line["unit_cents"], quantity, line.get("discount_percent", 0))
                            for line, quantity in zip(data["lines"], result["fulfilled"]))
print(json.dumps(result))
'''


class WorkflowExerciseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.stack = Path(__file__).resolve().parent.parent

    def prepare_case(self, case, name="project"):
        project = self.base / name
        output = prepare(case, self.stack, project)
        self.assertEqual(output["project"], str(project.resolve()))
        return project

    def fix_parser(self, project):
        (project / "labels.py").write_text(project_files("docs")["labels.py"], encoding="utf-8")
        (project / "tests/test_regression.py").write_text(normalized('''
            import unittest
            from labels import parse_labels


            class RegressionTests(unittest.TestCase):
                def test_whitespace_only_fields_are_omitted(self):
                    self.assertEqual(parse_labels(" ,a, ,b, "), ["a", "b"])
            '''), encoding="utf-8")

    def solve_modules(self, project):
        for name, source in (("pricing.py", PRICING_SOLUTION), ("inventory.py", INVENTORY_SOLUTION), ("order_report.py", REPORT_SOLUTION)):
            (project / name).write_text(normalized(source), encoding="utf-8")

    def test_prepare_is_deterministic_and_keeps_control_state_external(self):
        for case in CASES:
            with self.subTest(case=case):
                first = self.prepare_case(case, case + "-first")
                second = self.prepare_case(case, case + "-second")
                self.assertEqual(fingerprint(first), fingerprint(second))
                state = json.loads(manifest_path(first).read_text())
                self.assertEqual(state["starting_files"], fingerprint(first))
                self.assertNotIn(first, manifest_path(first).parents)
                self.assertFalse((first / "workflow_exercises.py").exists())
                self.assertFalse((first / "acceptance_check.py").exists())
                self.assertIn(".agents/skills/hoyelam-mode/SKILL.md", (first / "AGENTS.md").read_text())

    def test_prepare_refuses_existing_work_and_invalid_skill_without_writes(self):
        project = self.base / "occupied"
        project.mkdir()
        sentinel = project / "keep.txt"
        sentinel.write_text("user work")
        with self.assertRaisesRegex(ValueError, "new or empty"):
            prepare("docs", self.stack, project)
        self.assertEqual(sentinel.read_text(), "user work")
        self.assertFalse(manifest_path(project).exists())
        missing = self.base / "missing"
        with self.assertRaisesRegex(ValueError, "invalid skill"):
            prepare("docs", self.stack, missing, ["../outside"])
        self.assertFalse(missing.exists())

    def test_requested_skills_are_copied_without_changing_source(self):
        source = self.stack / "skills/hoyelam-mode/SKILL.md"
        previous = source.read_bytes()
        project = self.base / "minimal"
        prepare("docs", self.stack, project, ["prove-the-work"])
        self.assertEqual(sorted(path.name for path in (project / ".agents/skills").iterdir()), ["hoyelam-mode", "prove-the-work"])
        self.assertEqual(source.read_bytes(), previous)

    def test_docs_checker_requires_runnable_output_and_preserves_product_scope(self):
        project = self.prepare_case("docs")
        self.assertEqual(check("docs", project)["status"], "failed")
        readme = project / "README.md"
        readme.write_text(readme.read_text().replace("--output json", "--help"))
        self.assertEqual(check("docs", project)["status"], "failed")
        readme.write_text(project_files("harness")["README.md"])
        self.assertEqual(check("docs", project)["status"], "passed")
        with (project / "labels.py").open("a") as stream:
            stream.write("\nextra = True\n")
        self.assertIn("out-of-scope change: labels.py", check("docs", project)["problems"])

    def test_parser_checker_detects_regression_and_incomplete_fix(self):
        project = self.prepare_case("parser")
        self.assertEqual(check("parser", project)["status"], "failed")
        (project / "labels.py").write_text('def parse_labels(value):\n    return [part.strip() for part in value.split(",") if part and part != " "]\n')
        self.assertEqual(check("parser", project)["status"], "failed")
        self.fix_parser(project)
        before = fingerprint(project)
        self.assertEqual(check("parser", project)["status"], "passed")
        self.assertEqual(fingerprint(project), before)
        (project / "tests/test_regression.py").unlink()
        self.assertIn("candidate tests do not demonstrate the original parser regression", check("parser", project)["problems"])
        (project / "tests/test_labels.py").write_text("")
        self.assertIn("required unittest discovery was empty or skipped tests", check("parser", project)["problems"])

    def test_blocked_gate_cannot_be_manufactured_or_reported_as_passed(self):
        project = self.prepare_case("parser-blocked")
        self.fix_parser(project)
        result = check("parser-blocked", project)
        self.assertEqual(result["status"], "blocked")
        self.assertTrue(result["implementation_ok"])
        self.assertFalse(result["ok"])
        self.assertEqual(result["required_missing"], ["python3 acceptance_check.py"])
        (project / "acceptance_check.py").write_text('print("passed")\n')
        result = check("parser-blocked", project)
        self.assertEqual(result["status"], "failed")
        self.assertIn("externally supplied acceptance check was manufactured", result["problems"])

    def test_modules_checker_requires_domains_and_integration(self):
        project = self.prepare_case("modules")
        self.assertEqual(check("modules", project)["status"], "failed")
        self.solve_modules(project)
        self.assertEqual(check("modules", project)["status"], "passed")
        expected = {"total_cents": 725, "fulfilled": [2, 1, 1], "remaining": {"pen": 0, "book": 0}}
        (project / "order_report.py").write_text('print(' + repr(json.dumps(expected)) + ')\n')
        result = check("modules", project)
        self.assertEqual(result["status"], "failed")
        self.assertTrue(any("unexpected output" in problem for problem in result["problems"]))
        self.assertTrue(any("invalid input was not rejected" in problem for problem in result["problems"]))

    def test_harness_is_structurally_valid_before_runtime_repair(self):
        project = self.prepare_case("harness")
        validator = self.stack / "skills/build-verification-harness/scripts/validate_harness.py"
        validation = subprocess.run([sys.executable, str(validator), str(project / HARNESS)], capture_output=True, text=True)
        self.assertEqual(validation.returncode, 0, validation.stdout)
        product = subprocess.run([sys.executable, "label_cli.py", "split", "a,b", "--format", "json"], cwd=project, capture_output=True, text=True)
        self.assertEqual(json.loads(product.stdout), ["a", "b"])
        self.assertEqual(check("harness", project)["status"], "failed")
        mapping = project / HARNESS / "commands.json"
        commands = json.loads(mapping.read_text())
        commands["split"] = ["split"]
        mapping.write_text(json.dumps(commands))
        result = check("harness", project)
        self.assertEqual(result["status"], "passed", result["problems"])
        self.assertEqual(result["changed_files"], [f"{HARNESS}/commands.json"])
        self.assertFalse((project / "account.json").exists())
        (project / "account.json").write_text('{"name": "fake"}')
        self.assertIn("out-of-scope change: account.json", check("harness", project)["problems"])

    def test_harness_cannot_mutate_product_during_acceptance_checks(self):
        project = self.prepare_case("harness")
        mapping = project / HARNESS / "commands.json"
        mapping.write_text(json.dumps({"split": ["split"], "publish": ["publish"]}))
        control = project / HARNESS / "scripts/control.py"
        control.write_text(control.read_text().replace(
            'root = Path(__file__).resolve().parents[4]',
            'root = Path(__file__).resolve().parents[4]\n    product = root / "labels.py"\n    product.write_text(product.read_text() + "\\n")',
        ))
        result = check("harness", project)
        self.assertEqual(result["status"], "failed")
        self.assertIn("project files changed while acceptance checks were running", result["problems"])
        self.assertIn("out-of-scope change: labels.py", result["problems"])

    def test_cli_emits_json_and_distinct_blocked_exit_status(self):
        project = self.base / "cli-project"
        script = self.stack / "scripts/workflow_exercises.py"
        prepared = subprocess.run([sys.executable, str(script), "prepare", "--case", "parser-blocked", "--stack", str(self.stack), "--dest", str(project)], capture_output=True, text=True)
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        self.assertIn("prompt", json.loads(prepared.stdout))
        self.fix_parser(project)
        inspected = subprocess.run([sys.executable, str(script), "check", "--case", "parser-blocked", "--project", str(project)], capture_output=True, text=True)
        self.assertEqual(inspected.returncode, 2)
        self.assertEqual(json.loads(inspected.stdout)["status"], "blocked")

    def test_check_rejects_a_mismatched_manifest(self):
        project = self.prepare_case("docs")
        with self.assertRaisesRegex(ValueError, "does not identify"):
            check("parser", project)


if __name__ == "__main__":
    unittest.main()
