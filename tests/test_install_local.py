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


if __name__ == "__main__":
    unittest.main()
