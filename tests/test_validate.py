import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import (
    find_local_markdown_links,
    find_repository_references,
    find_scaffold_placeholders,
    parse_frontmatter,
    validate_marketplace,
    validate_repository,
)


class FrontmatterTests(unittest.TestCase):
    def test_parses_name_and_colon_in_description(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text("---\nname: example\ndescription: action: first\n---\n", encoding="utf-8")
            self.assertEqual(
                parse_frontmatter(path),
                {"name": "example", "description": "action: first"},
            )

    def test_requires_closing_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text("---\nname: example\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "closing"):
                parse_frontmatter(path)


class PlaceholderTests(unittest.TestCase):
    def test_finds_scaffold_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "unfinished.md"
            path.write_text("[" + "TODO: replace me]", encoding="utf-8")
            self.assertEqual(find_scaffold_placeholders(root), [path])


class ReferenceTests(unittest.TestCase):
    def test_resolves_local_markdown_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "SKILL.md"
            skill.write_text("[Reference](references/proof.md)\n[Web](https://example.com)\n", encoding="utf-8")
            self.assertEqual(find_local_markdown_links(skill), [(root / "references" / "proof.md").resolve()])

    def test_resolves_agent_repository_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agent = root / "agent.md"
            agent.write_text("Read `skills/verify-example/SKILL.md` and `agents/helper.md`.", encoding="utf-8")
            self.assertEqual(
                find_repository_references(agent, root),
                [
                    (root / "skills" / "verify-example" / "SKILL.md").resolve(),
                    (root / "agents" / "helper.md").resolve(),
                ],
            )


class RepositoryTests(unittest.TestCase):
    def test_hoyelam_stack_repository_is_valid(self) -> None:
        root = Path(__file__).resolve().parent.parent
        self.assertEqual(validate_repository(root), [])

    def test_ignores_local_state_and_git_metadata(self) -> None:
        source = Path(__file__).resolve().parent.parent
        for relative in (".work", ".hoyelam", ".git", "skills/hoyelam-mode/__pycache__"):
            with self.subTest(directory=relative), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "stack"
                shutil.copytree(
                    source, root,
                    ignore=shutil.ignore_patterns(".git", ".work", ".hoyelam", "__pycache__"),
                )
                scratch = root / relative
                scratch.mkdir(parents=True, exist_ok=True)
                (scratch / "draft.md").write_text(
                    "[Scratch reference](not-a-package-file.md)\n[" + "TODO: unfinished local note]\n",
                    encoding="utf-8",
                )
                self.assertEqual(validate_repository(root), [])

    def test_rejects_broken_links_outside_skill_entrypoints(self) -> None:
        source = Path(__file__).resolve().parent.parent
        for relative in (
            "docs/workflow.md",
            "skills/prove-the-work/references/project-verification.md",
            "agents/runtime-verifier.md",
            "automations/full-quality-pass/FOR_AGENTS.md",
        ):
            with self.subTest(path=relative):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "stack"
                    shutil.copytree(
                        source, root,
                        ignore=shutil.ignore_patterns(".git", ".work", ".hoyelam", "__pycache__"),
                    )
                    path = root / relative
                    original = path.read_text(encoding="utf-8")
                    target = path.parent / "missing-verification-contract.md"
                    path.write_text(original + "\n[Contract](missing-verification-contract.md)\n", encoding="utf-8")
                    issues = validate_repository(root)
                    self.assertEqual(len(issues), 1)
                    self.assertEqual(issues[0].path, path)
                    self.assertIn(str(target.resolve()), issues[0].message)
                    target.write_text(
                        "---\nname: verification-contract\ndescription: Resource validation fixture.\n---\n",
                        encoding="utf-8",
                    )
                    self.assertEqual(validate_repository(root), [])


class MarketplaceTests(unittest.TestCase):
    def test_rejects_a_marketplace_ref_that_does_not_match_the_plugin_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "marketplace.json"
            path.write_text(
                json.dumps(
                    {
                        "name": "hoyelam",
                        "interface": {"displayName": "Hoyelam"},
                        "plugins": [
                            {
                                "name": "hoyelam-stack",
                                "source": {
                                    "source": "url",
                                    "url": "https://github.com/hoyelam/hoyelam-stack.git",
                                    "ref": "v0.3.0",
                                },
                                "policy": {
                                    "installation": "AVAILABLE",
                                    "authentication": "ON_INSTALL",
                                },
                                "category": "Developer Tools",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            issues = validate_marketplace(path, "hoyelam-stack", "0.5.0")
            self.assertEqual(len(issues), 1)
            self.assertIn("v0.5.0", issues[0].message)


if __name__ == "__main__":
    unittest.main()
