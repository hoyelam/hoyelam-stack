from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parent.parent
        self.script = self.root / "skills" / "orchestrate-project" / "scripts" / "orchestrator.py"

    def run_command(
        self,
        store: Path,
        *arguments: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.script), "--store", str(store), *arguments],
            check=check,
            capture_output=True,
            text=True,
        )

    def initialize(self, store: Path) -> None:
        self.run_command(
            store,
            "init",
            "--goal",
            "Complete three durable units",
            "--done",
            "Three terminal units with current verification",
            "--standing-order",
            "Do not publish",
        )

    def add_unit(self, store: Path, identifier: str, dependency: str | None = None) -> None:
        arguments = [
            "unit",
            "add",
            identifier,
            "--goal",
            f"Complete {identifier}",
            "--scope",
            f"artifacts/{identifier}",
            "--acceptance",
            f"{identifier} exists",
            "--verify",
            f"verify {identifier}",
        ]
        if dependency is not None:
            arguments.extend(["--depends-on", dependency])
        self.run_command(store, *arguments)

    def finish_unit(self, store: Path, identifier: str, revision: str) -> None:
        self.run_command(store, "unit", "set", identifier, "--state", "verification", "--revision", revision)
        self.run_command(
            store,
            "verification",
            "record",
            identifier,
            "--revision",
            revision,
            "--verdict",
            "verified",
            "--evidence",
            f"verified {identifier}",
        )
        self.run_command(store, "unit", "set", identifier, "--state", "done")

    def test_three_unit_program_resumes_and_closes_with_current_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.add_unit(store, "unit-2", "unit-1")
            self.add_unit(store, "unit-3", "unit-2")

            self.finish_unit(store, "unit-1", "revision-1")
            first = self.run_command(
                store,
                "inbox",
                "push",
                "unit-1-complete",
                "--unit",
                "unit-1",
                "--status",
                "completed",
                "--report",
                "unit-1-report.json",
            )
            duplicate = self.run_command(
                store,
                "inbox",
                "push",
                "unit-1-complete",
                "--unit",
                "unit-1",
                "--status",
                "completed",
                "--report",
                "unit-1-report.json",
            )
            self.assertFalse(json.loads(first.stdout)["duplicate"])
            self.assertTrue(json.loads(duplicate.stdout)["duplicate"])
            self.assertEqual(len(json.loads(self.run_command(store, "inbox", "drain").stdout)), 1)
            processed_duplicate = self.run_command(
                store,
                "inbox",
                "push",
                "unit-1-complete",
                "--unit",
                "unit-1",
                "--status",
                "completed",
                "--report",
                "unit-1-report.json",
            )
            self.assertTrue(json.loads(processed_duplicate.stdout)["duplicate"])

            resumed = json.loads(self.run_command(store, "resume").stdout)
            self.assertEqual(resumed["counts"], {"done": 1, "pending": 2})
            self.assertEqual(resumed["ready"], ["unit-2"])
            self.assertEqual(resumed["units"][0]["verification"], "verified")

            self.finish_unit(store, "unit-2", "revision-1")
            self.run_command(store, "unit", "set", "unit-2", "--state", "verification", "--revision", "revision-2")
            stale = self.run_command(store, "verification", "check", "unit-2", check=False)
            self.assertEqual(stale.returncode, 1)
            self.assertIn("stale", stale.stderr)
            self.run_command(
                store,
                "verification",
                "record",
                "unit-2",
                "--revision",
                "revision-2",
                "--verdict",
                "verified",
                "--evidence",
                "verified updated unit-2",
            )
            self.run_command(store, "unit", "set", "unit-2", "--state", "done")
            self.finish_unit(store, "unit-3", "revision-1")

            closed = json.loads(self.run_command(store, "close").stdout)
            self.assertTrue(closed["can_close"])
            self.assertEqual(closed["counts"], {"done": 3})
            self.assertEqual(closed["program"]["status"], "complete")
            self.assertIn("Program status: complete", (store / "status.md").read_text(encoding="utf-8"))

    def test_concurrent_unit_writes_preserve_every_unit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            processes = []
            for index in range(12):
                identifier = f"parallel-{index}"
                processes.append(
                    subprocess.Popen(
                        [
                            str(self.script),
                            "--store",
                            str(store),
                            "unit",
                            "add",
                            identifier,
                            "--goal",
                            identifier,
                            "--scope",
                            identifier,
                            "--acceptance",
                            identifier,
                            "--verify",
                            identifier,
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                )
            results = [process.communicate(timeout=10) for process in processes]
            self.assertTrue(all(process.returncode == 0 for process in processes), results)
            status = json.loads(self.run_command(store, "status").stdout)
            self.assertEqual(status["unit_count"], 12)
            self.assertEqual(status["counts"], {"pending": 12})

    def test_close_rejects_missing_verification_and_open_gates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.run_command(store, "unit", "set", "unit-1", "--state", "verification", "--revision", "revision-1")
            missing = self.run_command(store, "unit", "set", "unit-1", "--state", "done", check=False)
            self.assertEqual(missing.returncode, 1)
            self.assertIn("verified evidence", missing.stderr)
            rejected = self.run_command(store, "close", check=False)
            self.assertEqual(rejected.returncode, 1)

            self.run_command(
                store,
                "verification",
                "record",
                "unit-1",
                "--revision",
                "revision-1",
                "--verdict",
                "verified",
                "--evidence",
                "verified unit-1",
            )
            self.run_command(store, "unit", "set", "unit-1", "--state", "done")
            self.run_command(store, "gate", "add", "decision", "--question", "Choose", "--default", "stop")
            gated = self.run_command(store, "close", check=False)
            self.assertEqual(gated.returncode, 1)
            self.run_command(store, "gate", "resolve", "decision", "--answer", "continue")
            first_close = self.run_command(store, "close")
            second_close = self.run_command(store, "close")
            first_completed_at = json.loads(first_close.stdout)["program"]["completed_at"]
            second_completed_at = json.loads(second_close.stdout)["program"]["completed_at"]
            self.assertEqual(first_completed_at, second_completed_at)
            mutation = self.run_command(store, "unit", "set", "unit-1", "--state", "running", check=False)
            self.assertEqual(mutation.returncode, 1)
            self.assertIn("closed", mutation.stderr)


if __name__ == "__main__":
    unittest.main()
