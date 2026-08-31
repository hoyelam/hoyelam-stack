from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class HarnessValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parent.parent
        self.script = (
            self.root
            / "skills"
            / "build-verification-harness"
            / "scripts"
            / "validate_harness.py"
        )

    def create_harness(self, root: Path) -> Path:
        skill = root / "verify-example"
        features = skill / "references" / "features"
        scripts = skill / "scripts"
        features.mkdir(parents=True)
        scripts.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: verify-example\ndescription: Verify the example app.\n---\n",
            encoding="utf-8",
        )
        (features / "README.md").write_text(
            "# Feature map\n\n- [Primary flow](primary-flow.md)\n",
            encoding="utf-8",
        )
        (features / "primary-flow.md").write_text(
            "# Primary flow\n\n"
            "## Sub-features\n\n- Entry\n\n"
            "## User path\n\nOpen it.\n\n"
            "## Harness drive\n\nRun it.\n\n"
            "## Proof\n\nObserve it.\n\n"
            "## Gotchas\n\nNone.\n",
            encoding="utf-8",
        )
        helper = scripts / "control.py"
        helper.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        helper.chmod(0o755)
        return skill

    def run_validator(self, skill: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.script), str(skill)],
            check=check,
            capture_output=True,
            text=True,
        )

    def test_accepts_complete_project_harness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.create_harness(Path(directory))
            result = json.loads(self.run_validator(skill).stdout)
            self.assertTrue(result["ok"])
            self.assertEqual(result["issues"], [])

    def test_reports_index_heading_and_executable_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.create_harness(Path(directory))
            features = skill / "references" / "features"
            (features / "README.md").write_text("# Feature map\n", encoding="utf-8")
            (features / "primary-flow.md").write_text("# Primary flow\n", encoding="utf-8")
            (skill / "scripts" / "control.py").chmod(0o644)

            completed = self.run_validator(skill, check=False)
            result = json.loads(completed.stdout)
            messages = [entry["message"] for entry in result["issues"]]

            self.assertEqual(completed.returncode, 1)
            self.assertFalse(result["ok"])
            self.assertIn("feature file is not linked from README.md", messages)
            self.assertIn("missing required heading: ## Proof", messages)
            self.assertIn("harness script must be executable", messages)

    def test_requires_name_in_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = self.create_harness(Path(directory))
            (skill / "SKILL.md").write_text(
                "Verify this app.\n\nname: verify-example\n",
                encoding="utf-8",
            )

            completed = self.run_validator(skill, check=False)
            result = json.loads(completed.stdout)

            self.assertEqual(completed.returncode, 1)
            self.assertIn(
                "skill name must start with verify-",
                [entry["message"] for entry in result["issues"]],
            )


if __name__ == "__main__":
    unittest.main()
