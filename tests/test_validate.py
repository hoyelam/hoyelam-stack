import tempfile
import unittest
from pathlib import Path

from scripts.validate import (
    find_local_markdown_links,
    find_repository_references,
    find_scaffold_placeholders,
    parse_frontmatter,
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


if __name__ == "__main__":
    unittest.main()
