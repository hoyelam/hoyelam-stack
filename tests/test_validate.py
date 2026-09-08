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
    validate_markdown_links,
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

    def test_validates_same_file_fragments_and_duplicate_heading_suffixes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "guide.md"
            content = (
                "# Status\n## Status\n## Status-1\n## Status\n"
                "[First](#status)\n[Second](#status-1)\n"
                "[Collision](#status-1-1)\n[Third](#status-2)\n"
            )
            path.write_text(content, encoding="utf-8")
            self.assertEqual(validate_markdown_links(path), [])

            path.write_text(content + "[Missing](#status-3)\n", encoding="utf-8")
            issues = validate_markdown_links(path)
            self.assertEqual(len(issues), 1)
            self.assertIn("#status-3", issues[0].message)

    def test_fenced_examples_supply_neither_headings_nor_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "guide.md"
            path.write_text(
                "````markdown\n# Example\n```\n# Still example\n"
                "[Example link](missing.md)\n````\n"
                "~~~markdown\n# Other example\n~~~\n"
                "# Real heading\n[Valid](#real-heading)\n"
                "[Missing](#example)\n[Also missing](#still-example)\n"
                "[Tilde example](#other-example)\n",
                encoding="utf-8",
            )
            issues = validate_markdown_links(path)
            self.assertEqual(len(issues), 3)
            for fragment in ("#example", "#still-example", "#other-example"):
                self.assertTrue(any(fragment in issue.message for issue in issues))

    def test_decodes_formatted_headings_and_ignores_external_fragments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "guide.md"
            target = root / "reference file.md"
            target.write_text("## Use `CLI` &amp; **tools** ###\n", encoding="utf-8")
            path.write_text(
                "[Local](reference%20file.md#use-cli--tools)\n"
                "[Web](https://example.com/reference.md#missing)\n"
                "[Web without scheme](//example.com/reference.md#missing)\n"
                "[Mail](mailto:example@example.com#fragment)\n",
                encoding="utf-8",
            )
            self.assertEqual(validate_markdown_links(path), [])


class RepositoryTests(unittest.TestCase):
    def test_hoyelam_stack_repository_is_valid(self) -> None:
        root = Path(__file__).resolve().parent.parent
        self.assertEqual(validate_repository(root), [])

    def test_rejects_missing_heading_in_existing_file_until_link_is_corrected(self) -> None:
        source = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "stack"
            shutil.copytree(
                source, root,
                ignore=shutil.ignore_patterns(".git", ".work", ".hoyelam", "__pycache__"),
            )
            reference = root / "docs" / "fragment-source.md"
            target = root / "docs" / "fragment-target.md"
            target.write_text("# Current section\n", encoding="utf-8")
            reference.write_text("[Details](fragment-target.md#old-section)\n", encoding="utf-8")

            issues = [issue for issue in validate_repository(root) if issue.path == reference]
            self.assertEqual(len(issues), 1)
            self.assertIn("#old-section", issues[0].message)

            reference.write_text("[Details](fragment-target.md#current-section)\n", encoding="utf-8")
            self.assertEqual(
                [issue for issue in validate_repository(root) if issue.path == reference],
                [],
            )

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
