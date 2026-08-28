from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


class DelegationRouterTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parent.parent
        self.script = root / "skills" / "hoyelam-mode" / "scripts" / "delegation_router.py"

    def route(self, *arguments: str) -> dict[str, object]:
        result = subprocess.run(
            ["python3", str(self.script), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_simple_operation_stays_with_parent(self) -> None:
        self.assertEqual(self.route()["children"], 0)

    def test_specialist_review_uses_one_child(self) -> None:
        result = self.route("--meaningful-streams", "1", "--specialist-review")
        self.assertEqual(result["children"], 1)

    def test_cross_repository_investigation_uses_two_children(self) -> None:
        result = self.route("--meaningful-streams", "2", "--repositories", "2")
        self.assertEqual(result["children"], 2)

    def test_high_risk_independent_units_use_three_children(self) -> None:
        result = self.route(
            "--meaningful-streams",
            "4",
            "--independent-units",
            "4",
            "--high-risk",
        )
        self.assertEqual(result["children"], 3)

    def test_repository_count_must_describe_a_real_task(self) -> None:
        result = subprocess.run(
            ["python3", str(self.script), "--repositories", "0"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("repositories must be at least one", result.stderr)

    def test_help_explains_routing_inputs_and_precedence(self) -> None:
        result = subprocess.run(
            ["python3", str(self.script), "--help"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("bounded evidence streams", result.stdout)
        self.assertIn("take precedence over cross-repository", result.stdout)


if __name__ == "__main__":
    unittest.main()
