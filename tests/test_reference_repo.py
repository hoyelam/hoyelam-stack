from __future__ import annotations

import importlib.util
import fcntl
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "investigate-first" / "scripts" / "reference_repo.py"
SPEC = importlib.util.spec_from_file_location("reference_repo", SCRIPT)
reference_repo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reference_repo)


class ReferenceRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source with spaces"
        self.source.mkdir()
        self.cache = self.root / "cache"
        self.git("init", "--initial-branch=main")
        self.first = self.commit("first")

    def git(self, *arguments: str, path: Path | None = None) -> str:
        return subprocess.run(
            ["git", "-C", str(path or self.source), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", *arguments],
            check=True, capture_output=True, text=True,
        ).stdout.strip()

    def commit(self, text: str) -> str:
        (self.source / "content.txt").write_text(text)
        self.git("add", "content.txt")
        self.git("commit", "-m", text)
        return self.git("rev-parse", "HEAD")

    def invoke(self, *arguments: str, ref: str = "main", source: Path | str | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(source or self.source), "--cache-dir", str(self.cache), f"--ref={ref}", *arguments],
            capture_output=True, text=True,
        )

    def checkout(self, *arguments: str, ref: str = "main") -> dict:
        result = self.invoke(*arguments, ref=ref)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_first_checkout_and_reuse_report_a_detached_revision(self) -> None:
        first = self.checkout()
        snapshot = Path(first["path"])
        self.assertEqual(first["revision"], self.first)
        self.assertEqual(first["cache_status"], "created")
        self.assertEqual(first["snapshot_status"], "created")
        self.assertEqual((snapshot / "content.txt").read_text(), "first")
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD", path=snapshot), "HEAD")
        reused = self.checkout()
        self.assertEqual(reused["path"], first["path"])
        self.assertEqual(reused["cache_status"], "reused")
        self.assertEqual(reused["snapshot_status"], "reused")

    def test_refresh_is_throttled_and_explicit_refresh_gets_new_commit(self) -> None:
        first = self.checkout()
        second = self.commit("second")
        self.assertEqual(self.checkout()["revision"], self.first)
        refreshed = self.checkout("--refresh")
        self.assertEqual(refreshed["revision"], second)
        self.assertEqual(refreshed["cache_status"], "refreshed")
        self.assertNotEqual(refreshed["path"], first["path"])
        self.assertEqual((Path(first["path"]) / "content.txt").read_text(), "first")

    def test_expired_cache_refreshes_branch(self) -> None:
        self.checkout()
        second = self.commit("second")
        refreshed = self.checkout("--refresh-interval", "0")
        self.assertEqual(refreshed["revision"], second)
        self.assertEqual(refreshed["cache_status"], "refreshed")

    def test_full_sha_stays_pinned_even_with_zero_refresh_interval(self) -> None:
        first = self.checkout(ref=self.first)
        self.commit("second")
        reused = self.checkout("--refresh-interval", "0", ref=self.first)
        self.assertEqual(reused["revision"], self.first)
        self.assertEqual(reused["path"], first["path"])
        self.assertEqual(reused["cache_status"], "reused")
        refreshed = self.checkout("--refresh", ref=self.first)
        self.assertEqual(refreshed["revision"], self.first)

    def test_tags_and_full_branch_refs_resolve(self) -> None:
        self.git("tag", "v1")
        self.assertEqual(self.checkout(ref="refs/heads/main")["revision"], self.first)
        self.assertEqual(self.checkout(ref="v1")["revision"], self.first)

    def test_dirty_source_is_preserved_and_only_committed_files_are_copied(self) -> None:
        (self.source / "content.txt").write_text("unfinished")
        (self.source / "untracked.txt").write_text("keep")
        result = self.checkout()
        self.assertEqual((self.source / "content.txt").read_text(), "unfinished")
        self.assertEqual((self.source / "untracked.txt").read_text(), "keep")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.first)
        self.assertEqual((Path(result["path"]) / "content.txt").read_text(), "first")
        self.assertFalse((Path(result["path"]) / "untracked.txt").exists())

    def test_dirty_snapshot_is_preserved_and_rejected(self) -> None:
        snapshot = Path(self.checkout()["path"])
        (snapshot / "content.txt").write_text("edited")
        (snapshot / "untracked.txt").write_text("keep")
        result = self.invoke()
        self.assertEqual(result.returncode, 1)
        self.assertIn("local changes", json.loads(result.stderr)["error"])
        self.assertEqual((snapshot / "content.txt").read_text(), "edited")
        self.assertEqual((snapshot / "untracked.txt").read_text(), "keep")

    def test_snapshot_switched_to_a_branch_is_preserved_and_rejected(self) -> None:
        snapshot = Path(self.checkout()["path"])
        self.git("switch", "-c", "local-work", path=snapshot)
        result = self.invoke()
        self.assertEqual(result.returncode, 1)
        self.assertIn("no longer detached", result.stderr)
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD", path=snapshot), "local-work")

    def test_concurrent_initial_requests_share_one_valid_snapshot(self) -> None:
        command = [sys.executable, str(SCRIPT), str(self.source), "--cache-dir", str(self.cache), "--ref", "main"]
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
        results = []
        for process in processes:
            stdout, stderr = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, stderr)
            results.append(json.loads(stdout))
        self.assertEqual({result["cache_status"] for result in results}, {"created", "reused"})
        self.assertEqual(results[0]["path"], results[1]["path"])
        self.assertEqual(results[0]["revision"], self.first)

    def test_lock_timeout_reports_existing_work_without_altering_snapshot(self) -> None:
        snapshot = Path(self.checkout()["path"])
        with (snapshot.parents[1] / "lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.invoke("--timeout", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Another process", result.stderr)
        self.assertEqual((snapshot / "content.txt").read_text(), "first")

    def test_command_timeout_is_reported(self) -> None:
        started = time.monotonic()
        with self.assertRaisesRegex(reference_repo.CacheError, "exceeded 1s"):
            reference_repo.run([
                sys.executable, "-c",
                "import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(10)']); time.sleep(10)",
            ], 1)
        self.assertLess(time.monotonic() - started, 5)

    def test_untracked_and_ignored_snapshot_files_are_rejected(self) -> None:
        (self.source / ".gitignore").write_text("ignored.txt\n")
        self.git("add", ".gitignore")
        self.git("commit", "-m", "ignore fixture")
        snapshot = Path(self.checkout()["path"])
        for name in ("untracked.txt", "ignored.txt"):
            with self.subTest(name=name):
                target = snapshot / name
                target.write_text("keep")
                result = self.invoke()
                self.assertEqual(result.returncode, 1)
                self.assertIn("local changes", result.stderr)
                self.assertEqual(target.read_text(), "keep")
                target.unlink()

    def test_failed_refresh_reports_error_and_leaves_snapshot_unchanged(self) -> None:
        snapshot = Path(self.checkout()["path"])
        moved = self.source.with_name("unavailable-source")
        self.source.rename(moved)
        self.source.mkdir()
        result = self.invoke("--refresh")
        self.assertEqual(result.returncode, 1)
        self.assertIn("git exited", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual((snapshot / "content.txt").read_text(), "first")

    def test_failed_initial_clone_can_be_retried(self) -> None:
        invalid = self.root / "not-a-repository"
        invalid.mkdir()
        failed = self.invoke(source=invalid)
        self.assertEqual(failed.returncode, 1)
        self.assertIn("git exited", failed.stderr)
        self.git("init", "--bare", path=invalid)
        self.git("push", str(invalid), "main")
        retried = self.invoke(source=invalid)
        self.assertEqual(retried.returncode, 0, retried.stderr)
        self.assertEqual(json.loads(retried.stdout)["revision"], self.first)

    def test_invalid_refs_fail_before_creating_cache(self) -> None:
        for ref in ("--help", "main~1", "main^{tree}", "main:content.txt", "../main", "main@{0}", ""):
            with self.subTest(ref=ref):
                result = self.invoke(ref=ref)
                self.assertEqual(result.returncode, 1)
                self.assertIn("--ref must be", result.stderr)
        self.assertFalse(self.cache.exists())

    def test_missing_ref_is_an_actionable_error(self) -> None:
        result = self.invoke(ref="absent")
        self.assertEqual(result.returncode, 1)
        self.assertIn("unavailable", json.loads(result.stderr)["error"])
        self.assertIn("--refresh", result.stderr)

    def test_abbreviated_sha_and_ambiguous_ref_require_explicit_revision(self) -> None:
        self.git("tag", "main")
        for ref in (self.first[:8], "main"):
            with self.subTest(ref=ref):
                result = self.invoke(ref=ref)
                self.assertEqual(result.returncode, 1)
                self.assertIn("unambiguous", result.stderr)
        self.assertEqual(self.checkout(ref="refs/heads/main")["revision"], self.first)

    def test_corrupt_metadata_does_not_replace_existing_snapshot(self) -> None:
        snapshot = Path(self.checkout()["path"])
        state = snapshot.parents[1] / "state.json"
        state.write_text("invalid json")
        result = self.invoke()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid cache metadata", result.stderr)
        self.assertEqual((snapshot / "content.txt").read_text(), "first")

    def test_github_uses_gh_initial_clone_and_preserves_explicit_url(self) -> None:
        source = "https://github.com/owner/repo.git"
        resolved, remote, github = reference_repo.resolve_source(source)
        self.assertEqual(reference_repo.clone_command(resolved, Path("destination"), remote, github), [
            "gh", "repo", "clone", source, "destination", "--", "--bare", "--filter=blob:none",
        ])

    def test_invalid_remote_inputs_are_rejected_without_network(self) -> None:
        for source in (
            "https://github.com/owner/repo/tree/main", "https://github.com/owner/repo/blob/main/file",
            "https://github.com/owner/repo?ref=main", "https://name:secret@example.invalid/repo",
            "http://example.invalid/repo", "owner/repo",
        ):
            with self.subTest(source=source):
                result = self.invoke(source=source)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
        self.assertFalse(self.cache.exists())

    def test_refresh_and_timeout_arguments_are_bounded(self) -> None:
        for argument, value in (("--refresh-interval", "-1"), ("--refresh-interval", "86401"), ("--timeout", "0"), ("--timeout", "301")):
            with self.subTest(argument=argument, value=value):
                result = self.invoke(argument, value)
                self.assertEqual(result.returncode, 2)
                self.assertIn("between", result.stderr)


if __name__ == "__main__":
    unittest.main()
