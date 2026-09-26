import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class InstallLocalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parent.parent
        self.script = self.root / "scripts" / "install-local.sh"

    def environment(self, directory: Path) -> dict[str, str]:
        environment = os.environ.copy()
        environment["HOYELAM_STACK_CODEX_SKILLS_ROOT"] = str(directory / "codex")
        return environment

    def test_installs_codex_skills_idempotently(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            environment = self.environment(destination)
            first = subprocess.run(
                [str(self.script)],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            second = subprocess.run(
                [str(self.script)],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertIn("Linked:", first.stdout)
            self.assertIn("Already linked:", second.stdout)
            skill_names = {path.parent.name for path in (self.root / "skills").glob("*/SKILL.md")}
            linked_names = {path.name for path in (destination / "codex").iterdir()}
            self.assertEqual(linked_names, skill_names)

    def test_refuses_existing_destination(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            conflict = destination / "codex" / "comment-discipline"
            conflict.mkdir(parents=True)
            result = subprocess.run(
                [str(self.script)],
                check=False,
                capture_output=True,
                text=True,
                env=self.environment(destination),
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Conflict:", result.stderr)
            self.assertTrue(conflict.is_dir())

    def test_reinstall_through_repository_alias_preserves_existing_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            alias = destination / "repository-alias"
            alias.symlink_to(self.root, target_is_directory=True)
            environment = self.environment(destination)
            subprocess.run(
                [str(alias / "scripts/install-local.sh")],
                check=True, capture_output=True, text=True, env=environment,
            )
            links = {path: os.readlink(path) for path in (destination / "codex").iterdir()}
            self.assertTrue(all(target.startswith(str(alias)) for target in links.values()))
            result = subprocess.run(
                [str(self.script)],
                check=False, capture_output=True, text=True, env=environment,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({path: os.readlink(path) for path in links}, links)
            for path in links:
                self.assertTrue(path.samefile(self.root / "skills" / path.name))

    def test_accepts_relative_link_to_same_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory).resolve()
            target = destination / "codex" / "comment-discipline"
            target.parent.mkdir()
            relative = os.path.relpath(self.root / "skills" / target.name, target.parent)
            target.symlink_to(relative, target_is_directory=True)
            self.assertTrue(target.samefile(self.root / "skills" / target.name))
            result = subprocess.run(
                [str(self.script)], check=False, capture_output=True, text=True,
                env=self.environment(destination),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(os.readlink(target), relative)

    def test_refuses_unrelated_and_dangling_symlinks_without_replacing_them(self) -> None:
        for exists in (True, False):
            with self.subTest(exists=exists), tempfile.TemporaryDirectory() as directory:
                destination = Path(directory)
                unrelated = destination / "other-skill"
                if exists:
                    unrelated.mkdir()
                target = destination / "codex" / "comment-discipline"
                target.parent.mkdir()
                target.symlink_to(unrelated, target_is_directory=True)
                result = subprocess.run(
                    [str(self.script)], check=False, capture_output=True, text=True,
                    env=self.environment(destination),
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn(str(target), result.stderr)
                self.assertTrue(target.is_symlink())
                self.assertEqual(os.readlink(target), str(unrelated))


if __name__ == "__main__":
    unittest.main()
