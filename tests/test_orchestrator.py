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
            self.assertEqual(resumed["units"][0]["latest_report"]["report"], "unit-1-report.json")
            self.assertEqual(resumed["units"][0]["latest_report"]["queue"], "processed")
            self.assertIn("unit-1-report.json", (store / "status.md").read_text(encoding="utf-8"))

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

    def test_verification_records_structured_harness_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.run_command(
                store,
                "unit",
                "set",
                "unit-1",
                "--state",
                "verification",
                "--revision",
                "revision-1",
            )

            recorded = json.loads(
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
                    "captured the user-visible result",
                    "--harness",
                    "verify-app",
                    "--harness-revision",
                    "harness-revision-1",
                    "--doctor",
                    "passed",
                    "--feature",
                    "primary-flow",
                    "--artifact",
                    "artifacts/primary-flow.json",
                ).stdout
            )

            self.assertEqual(
                recorded["harness"],
                {
                    "name": "verify-app",
                    "revision": "harness-revision-1",
                    "doctor": "passed",
                    "features": ["primary-flow"],
                    "artifacts": ["artifacts/primary-flow.json"],
                },
            )
            checked = json.loads(
                self.run_command(store, "verification", "check", "unit-1").stdout
            )
            self.assertEqual(checked["harness"], recorded["harness"])

    def test_verified_harness_evidence_requires_behavior_and_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.run_command(
                store,
                "unit",
                "set",
                "unit-1",
                "--state",
                "verification",
                "--revision",
                "revision-1",
            )

            incomplete = self.run_command(
                store,
                "verification",
                "record",
                "unit-1",
                "--revision",
                "revision-1",
                "--verdict",
                "verified",
                "--evidence",
                "doctor only",
                "--harness",
                "verify-app",
                "--harness-revision",
                "harness-revision-1",
                "--doctor",
                "passed",
                check=False,
            )

            self.assertEqual(incomplete.returncode, 1)
            self.assertIn("at least one --feature", incomplete.stderr)
            self.assertEqual((store / "verification.json").read_text(encoding="utf-8").strip(), "[]")

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

    def test_assignments_track_attempts_threads_and_exclusive_scope_leases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.add_unit(store, "unit-2")

            first = json.loads(
                self.run_command(
                    store,
                    "unit",
                    "assign",
                    "unit-1",
                    "--worker",
                    "reviewer",
                    "--thread",
                    "/root/reviewer",
                    "--lease",
                    "repo:shared-source",
                ).stdout
            )
            repeated = json.loads(
                self.run_command(
                    store,
                    "unit",
                    "assign",
                    "unit-1",
                    "--worker",
                    "reviewer",
                    "--thread",
                    "/root/reviewer",
                    "--lease",
                    "repo:shared-source",
                ).stdout
            )
            self.assertEqual(first["assignment"]["attempt"], 1)
            self.assertEqual(first["assignment"]["thread"], "/root/reviewer")
            self.assertEqual(len(repeated["attempts"]), 1)
            report = json.loads(
                self.run_command(
                    store,
                    "inbox",
                    "push",
                    "unit-1-attempt-1",
                    "--unit",
                    "unit-1",
                    "--status",
                    "completed",
                    "--report",
                    "unit-1-report.json",
                    "--worker",
                    "reviewer",
                    "--thread",
                    "/root/reviewer",
                    "--attempt",
                    "1",
                ).stdout
            )
            self.assertEqual(report["attempt"], 1)
            self.assertEqual(report["thread"], "/root/reviewer")
            self.run_command(store, "inbox", "drain")

            conflict = self.run_command(
                store,
                "unit",
                "assign",
                "unit-2",
                "--worker",
                "implementer",
                "--thread",
                "/root/implementer",
                "--lease",
                "repo:shared-source",
                check=False,
            )
            self.assertEqual(conflict.returncode, 1)
            self.assertIn("scope lease is owned by unit-1", conflict.stderr)

            released = json.loads(
                self.run_command(
                    store,
                    "unit",
                    "release",
                    "unit-1",
                    "--outcome",
                    "completed",
                    "--revision",
                    "revision-1",
                    "--worker",
                    "reviewer",
                    "--thread",
                    "/root/reviewer",
                    "--attempt",
                    "1",
                ).stdout
            )
            self.assertIsNone(released["assignment"])
            self.assertEqual(released["attempts"][0]["outcome"], "completed")
            self.assertEqual(released["state"], "verification")
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
                "verified assigned unit",
            )
            self.run_command(store, "unit", "set", "unit-1", "--state", "done")

            assigned = json.loads(
                self.run_command(
                    store,
                    "unit",
                    "assign",
                    "unit-2",
                    "--worker",
                    "implementer",
                    "--thread",
                    "/root/implementer",
                    "--lease",
                    "repo:shared-source",
                ).stdout
            )
            self.assertEqual(assigned["assignment"]["attempt"], 1)
            self.run_command(
                store,
                "unit",
                "release",
                "unit-2",
                "--outcome",
                "failed",
                "--worker",
                "implementer",
                "--thread",
                "/root/implementer",
                "--attempt",
                "1",
            )
            retried = json.loads(
                self.run_command(
                    store,
                    "unit",
                    "assign",
                    "unit-2",
                    "--worker",
                    "implementer",
                    "--thread",
                    "/root/implementer",
                    "--lease",
                    "repo:shared-source",
                ).stdout
            )
            self.assertEqual(retried["assignment"]["attempt"], 2)
            self.assertEqual(len(retried["attempts"]), 2)
            late = json.loads(
                self.run_command(
                    store,
                    "inbox",
                    "push",
                    "unit-2-attempt-1-late",
                    "--unit",
                    "unit-2",
                    "--status",
                    "failed",
                    "--report",
                    "unit-2-attempt-1.json",
                    "--attempt",
                    "1",
                    "--worker",
                    "implementer",
                    "--thread",
                    "/root/implementer",
                ).stdout
            )
            self.assertEqual(late["attempt"], 1)
            self.assertEqual(late["thread"], "/root/implementer")
            self.run_command(store, "inbox", "drain")

            resumed = json.loads(self.run_command(store, "resume").stdout)
            self.assertEqual(
                resumed["active_leases"],
                [
                    {
                        "attempt": 2,
                        "scope": "repo:shared-source",
                        "thread": "/root/implementer",
                        "unit": "unit-2",
                        "worker": "implementer",
                    }
                ],
            )
            self.assertIn("/root/implementer", (store / "status.md").read_text(encoding="utf-8"))

    def test_release_rejects_stale_attempt_identity_after_reassignment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.run_command(
                store,
                "unit",
                "assign",
                "unit-1",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--lease",
                "repo:unit-1",
            )
            self.run_command(
                store,
                "unit",
                "release",
                "unit-1",
                "--outcome",
                "failed",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--attempt",
                "1",
            )
            self.run_command(
                store,
                "unit",
                "assign",
                "unit-1",
                "--worker",
                "worker",
                "--thread",
                "thread-2",
                "--lease",
                "repo:unit-1",
            )

            stale = self.run_command(
                store,
                "unit",
                "release",
                "unit-1",
                "--outcome",
                "completed",
                "--revision",
                "stale-revision",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--attempt",
                "1",
                check=False,
            )
            self.assertEqual(stale.returncode, 1)
            self.assertIn("does not match active assignment", stale.stderr)
            status = json.loads(self.run_command(store, "status").stdout)
            unit = status["units"][0]
            self.assertEqual(unit["state"], "running")
            self.assertEqual(unit["assignment"]["attempt"], 2)
            self.assertEqual(unit["revision"], "")

    def test_inbox_identity_is_explicit_and_duplicate_is_stable_across_retries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            assignment = [
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--lease",
                "repo:unit-1",
            ]
            self.run_command(store, "unit", "assign", "unit-1", *assignment)
            event = [
                "inbox",
                "push",
                "attempt-1-report",
                "--unit",
                "unit-1",
                "--status",
                "failed",
                "--report",
                "attempt-1.json",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--attempt",
                "1",
            ]
            first = json.loads(self.run_command(store, *event).stdout)
            self.assertFalse(first["duplicate"])
            self.run_command(
                store,
                "unit",
                "release",
                "unit-1",
                "--outcome",
                "failed",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--attempt",
                "1",
            )
            self.run_command(store, "unit", "assign", "unit-1", *assignment)

            duplicate = json.loads(self.run_command(store, *event).stdout)
            self.assertTrue(duplicate["duplicate"])
            omitted = self.run_command(
                store,
                "inbox",
                "push",
                "ambiguous-report",
                "--unit",
                "unit-1",
                "--status",
                "completed",
                "--report",
                "ambiguous.json",
                check=False,
            )
            self.assertEqual(omitted.returncode, 1)
            self.assertIn("requires worker, thread, and attempt", omitted.stderr)

    def test_legacy_inbox_duplicate_remains_idempotent_after_assignment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            event = [
                "inbox",
                "push",
                "legacy-event",
                "--unit",
                "unit-1",
                "--status",
                "completed",
                "--report",
                "legacy.json",
            ]
            self.run_command(store, *event)
            event_path = store / "inbox" / "pending" / "legacy-event.json"
            payload = json.loads(event_path.read_text(encoding="utf-8"))
            for key in ("worker", "thread", "attempt"):
                payload.pop(key)
            event_path.write_text(json.dumps(payload), encoding="utf-8")
            self.run_command(
                store,
                "unit",
                "assign",
                "unit-1",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--lease",
                "repo:unit-1",
            )

            duplicate = json.loads(self.run_command(store, *event).stdout)
            self.assertTrue(duplicate["duplicate"])

    def test_status_escapes_markdown_table_delimiters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.run_command(
                store,
                "inbox",
                "push",
                "report",
                "--unit",
                "unit-1",
                "--status",
                "completed",
                "--report",
                "artifacts/a|b.json",
            )
            self.run_command(store, "status")
            status = (store / "status.md").read_text(encoding="utf-8")
            self.assertIn("artifacts/a\\|b.json", status)
            self.assertNotIn("artifacts/a|b.json", status)

    def test_repository_scope_leases_reject_hierarchical_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            for identifier in ("parent", "child", "sibling"):
                self.add_unit(store, identifier)
            self.run_command(
                store,
                "unit",
                "assign",
                "parent",
                "--worker",
                "parent",
                "--thread",
                "thread-parent",
                "--lease",
                "repo:src",
            )
            overlap = self.run_command(
                store,
                "unit",
                "assign",
                "child",
                "--worker",
                "child",
                "--thread",
                "thread-child",
                "--lease",
                "repo:src/file.py",
                check=False,
            )
            self.assertEqual(overlap.returncode, 1)
            self.assertIn("scope lease is owned by parent", overlap.stderr)
            sibling = json.loads(
                self.run_command(
                    store,
                    "unit",
                    "assign",
                    "sibling",
                    "--worker",
                    "sibling",
                    "--thread",
                    "thread-sibling",
                    "--lease",
                    "repo:source",
                ).stdout
            )
            self.assertEqual(sibling["assignment"]["leases"], ["repo:source"])
            noncanonical = self.run_command(
                store,
                "unit",
                "assign",
                "child",
                "--worker",
                "child",
                "--thread",
                "thread-child",
                "--lease",
                "repo:src/../other",
                check=False,
            )
            self.assertEqual(noncanonical.returncode, 1)
            self.assertIn("already be canonical", noncanonical.stderr)

    def test_existing_unit_without_assignment_fields_upgrades_on_first_assignment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            units_path = store / "units.json"
            units = json.loads(units_path.read_text(encoding="utf-8"))
            units["unit-1"].pop("assignment")
            units["unit-1"].pop("attempts")
            units_path.write_text(json.dumps(units), encoding="utf-8")

            assigned = json.loads(
                self.run_command(
                    store,
                    "unit",
                    "assign",
                    "unit-1",
                    "--worker",
                    "worker",
                    "--thread",
                    "thread-1",
                    "--lease",
                    "repo:unit-1",
                ).stdout
            )
            self.assertEqual(assigned["assignment"]["attempt"], 1)
            self.assertEqual(len(assigned["attempts"]), 1)

    def test_assignment_requires_ready_dependencies_and_release_before_state_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.add_unit(store, "unit-2", "unit-1")

            dependency = self.run_command(
                store,
                "unit",
                "assign",
                "unit-2",
                "--worker",
                "worker",
                "--thread",
                "thread-2",
                "--lease",
                "repo:unit-2",
                check=False,
            )
            self.assertEqual(dependency.returncode, 1)
            self.assertIn("incomplete dependencies", dependency.stderr)

            self.run_command(
                store,
                "unit",
                "assign",
                "unit-1",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--lease",
                "repo:unit-1",
            )
            state_change = self.run_command(
                store,
                "unit",
                "set",
                "unit-1",
                "--state",
                "blocked",
                check=False,
            )
            self.assertEqual(state_change.returncode, 1)
            self.assertIn("release the active assignment", state_change.stderr)

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

    def test_blank_revision_cannot_be_released_verified_or_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.run_command(
                store,
                "unit",
                "assign",
                "unit-1",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--lease",
                "repo:unit-1",
            )

            release = self.run_command(
                store,
                "unit",
                "release",
                "unit-1",
                "--outcome",
                "completed",
                "--revision",
                " ",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--attempt",
                "1",
                check=False,
            )
            self.assertEqual(release.returncode, 1)
            self.assertIn("must be one non-empty line", release.stderr)
            verification = self.run_command(
                store,
                "verification",
                "record",
                "unit-1",
                "--revision",
                " ",
                "--verdict",
                "verified",
                "--evidence",
                "invalid",
                check=False,
            )
            self.assertEqual(verification.returncode, 1)
            self.assertIn("must be one non-empty line", verification.stderr)
            closed = self.run_command(store, "close", check=False)
            self.assertEqual(closed.returncode, 1)

    def test_corrupted_store_fails_cleanly_before_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            units_path = store / "units.json"
            gates_path = store / "gates.json"
            units_before = units_path.read_bytes()
            gates_path.write_text("[]\n", encoding="utf-8")

            assignment = self.run_command(
                store,
                "unit",
                "assign",
                "unit-1",
                "--worker",
                "worker",
                "--thread",
                "thread-1",
                "--lease",
                "repo:unit-1",
                check=False,
            )
            self.assertEqual(assignment.returncode, 1)
            self.assertNotIn("Traceback", assignment.stderr)
            self.assertIn("gates.json must contain an object", assignment.stderr)
            self.assertEqual(units_path.read_bytes(), units_before)

            gates_path.write_text("{}\n", encoding="utf-8")
            units = json.loads(units_path.read_text(encoding="utf-8"))
            units["unit-1"].pop("id")
            units_path.write_text(json.dumps(units), encoding="utf-8")
            resumed = self.run_command(store, "resume", check=False)
            self.assertEqual(resumed.returncode, 1)
            self.assertNotIn("Traceback", resumed.stderr)
            self.assertIn("missing fields: id", resumed.stderr)

    def test_inbox_drain_is_preflighted_and_never_overwrites_processed_event(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            for event in ("first", "second"):
                self.run_command(
                    store,
                    "inbox",
                    "push",
                    event,
                    "--unit",
                    "unit-1",
                    "--status",
                    "completed",
                    "--report",
                    f"{event}.json",
                )
            pending = store / "inbox" / "pending"
            processed = store / "inbox" / "processed"
            second_path = pending / "second.json"
            second_payload = second_path.read_bytes()
            second_path.write_text("{}\n", encoding="utf-8")

            malformed = self.run_command(store, "inbox", "drain", check=False)
            self.assertEqual(malformed.returncode, 1)
            self.assertNotIn("Traceback", malformed.stderr)
            self.assertTrue((pending / "first.json").exists())
            self.assertTrue(second_path.exists())
            self.assertEqual(list(processed.glob("*.json")), [])

            second_path.write_bytes(second_payload)
            processed_first = processed / "first.json"
            processed_payload = (pending / "first.json").read_bytes()
            processed_first.write_bytes(processed_payload)
            duplicate = self.run_command(store, "inbox", "drain", check=False)
            self.assertEqual(duplicate.returncode, 1)
            self.assertIn("multiple queues", duplicate.stderr)
            self.assertEqual(processed_first.read_bytes(), processed_payload)
            self.assertTrue((pending / "first.json").exists())

    def test_invalid_attempt_history_gate_and_evidence_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            self.add_unit(store, "unit-1")
            self.run_command(store, "unit", "set", "unit-1", "--state", "verification", "--revision", "r1")
            blank_evidence = self.run_command(
                store,
                "verification",
                "record",
                "unit-1",
                "--revision",
                "r1",
                "--verdict",
                "verified",
                "--evidence",
                " ",
                check=False,
            )
            self.assertEqual(blank_evidence.returncode, 1)
            self.assertIn("non-empty string", blank_evidence.stderr)

            self.add_unit(store, "unit-2")
            self.run_command(
                store,
                "unit",
                "assign",
                "unit-2",
                "--worker",
                "worker",
                "--thread",
                "thread-2",
                "--lease",
                "repo:unit-2",
            )
            units_path = store / "units.json"
            valid_units = units_path.read_bytes()
            units = json.loads(valid_units)
            units["unit-2"]["attempts"].append(dict(units["unit-2"]["attempts"][0]))
            units_path.write_text(json.dumps(units), encoding="utf-8")
            invalid_attempt = self.run_command(
                store,
                "unit",
                "release",
                "unit-2",
                "--outcome",
                "failed",
                "--worker",
                "worker",
                "--thread",
                "thread-2",
                "--attempt",
                "1",
                check=False,
            )
            self.assertEqual(invalid_attempt.returncode, 1)
            self.assertNotIn("Traceback", invalid_attempt.stderr)
            self.assertIn("only the latest attempt may be unfinished", invalid_attempt.stderr)
            units_path.write_bytes(valid_units)

            gates_path = store / "gates.json"
            gates_path.write_text(
                json.dumps(
                    {
                        "decision": {
                            "id": "decision",
                            "question": "Choose",
                            "default": "stop",
                            "answer": None,
                            "created_at": "time",
                            "resolved_at": None,
                        }
                    }
                ),
                encoding="utf-8",
            )
            program_before = (store / "program.json").read_bytes()
            closed = self.run_command(store, "close", check=False)
            self.assertEqual(closed.returncode, 1)
            self.assertNotIn("Traceback", closed.stderr)
            self.assertIn("missing fields: status", closed.stderr)
            self.assertEqual((store / "program.json").read_bytes(), program_before)

    def test_resume_removes_orphan_atomic_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = Path(directory) / "store"
            self.initialize(store)
            root_temporary = store / ".hoyelam-tmp"
            inbox_temporary = store / "inbox" / "pending" / ".hoyelam-tmp"
            root_temporary.mkdir(exist_ok=True)
            inbox_temporary.mkdir(exist_ok=True)
            root_orphan = root_temporary / "units.json.orphan"
            inbox_orphan = inbox_temporary / "event.json.orphan"
            root_backup = store / ".units.json.backup"
            inbox_backup = store / "inbox" / "pending" / ".manual.json.backup"
            root_orphan.write_text("partial", encoding="utf-8")
            inbox_orphan.write_text("partial", encoding="utf-8")
            root_backup.write_text("keep", encoding="utf-8")
            inbox_backup.write_text("keep", encoding="utf-8")

            self.run_command(store, "resume")
            self.assertFalse(root_orphan.exists())
            self.assertFalse(inbox_orphan.exists())
            self.assertEqual(root_backup.read_text(encoding="utf-8"), "keep")
            self.assertEqual(inbox_backup.read_text(encoding="utf-8"), "keep")

    def test_runtime_temporary_directory_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            store = base / "store"
            outside = base / "outside"
            outside.mkdir()
            sentinel = outside / "sentinel.txt"
            sentinel.write_text("keep", encoding="utf-8")
            self.initialize(store)
            temporary = store / ".hoyelam-tmp"
            temporary.rmdir()
            temporary.symlink_to(outside, target_is_directory=True)

            resumed = self.run_command(store, "resume", check=False)
            self.assertEqual(resumed.returncode, 1)
            self.assertNotIn("Traceback", resumed.stderr)
            self.assertIn("not a real directory", resumed.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
