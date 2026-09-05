from __future__ import annotations

import json
import os
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ValidationIssue:
    path: Path
    message: str


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter boundary")
    boundary = text.find("\n---\n", 4)
    if boundary == -1:
        raise ValueError("missing closing frontmatter boundary")
    result: dict[str, str] = {}
    for line in text[4:boundary].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def repository_files(root: Path) -> Iterator[Path]:
    excluded = {".git", ".work", ".hoyelam", "__pycache__"}
    for directory, directories, filenames in os.walk(root):
        directories[:] = [name for name in directories if name not in excluded]
        for name in filenames:
            path = Path(directory) / name
            if path.is_file():
                yield path


def find_scaffold_placeholders(root: Path) -> list[Path]:
    suffixes = {".md", ".json", ".yaml", ".yml", ".py", ".sh"}
    marker = "[" + "TODO:"
    found: list[Path] = []
    for path in repository_files(root):
        if path.suffix in suffixes:
            if marker in path.read_text(encoding="utf-8"):
                found.append(path)
    return found


def find_local_markdown_links(path: Path) -> list[Path]:
    links: list[Path] = []
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        location = target.split("#", 1)[0]
        if not location or "://" in location or location.startswith("mailto:"):
            continue
        links.append((path.parent / location).resolve())
    return links


def find_repository_references(path: Path, root: Path) -> list[Path]:
    references = re.findall(r"`((?:skills|agents)/[^`]+)`", path.read_text(encoding="utf-8"))
    return [(root / reference).resolve() for reference in references]


def validate_marketplace(path: Path, plugin_name: str, plugin_version: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        marketplace = load_json(path)
    except (ValueError, json.JSONDecodeError) as error:
        return [ValidationIssue(path, str(error))]

    interface = marketplace.get("interface")
    if not isinstance(marketplace.get("name"), str) or not marketplace["name"]:
        issues.append(ValidationIssue(path, "marketplace name is missing"))
    if not isinstance(interface, dict) or not interface.get("displayName"):
        issues.append(ValidationIssue(path, "marketplace display name is missing"))

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        return issues + [ValidationIssue(path, "marketplace plugins must be a list")]
    matching = [entry for entry in plugins if isinstance(entry, dict) and entry.get("name") == plugin_name]
    if len(matching) != 1:
        return issues + [ValidationIssue(path, f"marketplace must contain exactly one {plugin_name} entry")]

    entry = matching[0]
    source = entry.get("source")
    expected_source = {
        "source": "url",
        "url": "https://github.com/hoyelam/hoyelam-stack.git",
        "ref": f"v{plugin_version}",
    }
    if source != expected_source:
        issues.append(ValidationIssue(path, f"marketplace source must be {expected_source}"))
    expected_policy = {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
    if entry.get("policy") != expected_policy:
        issues.append(ValidationIssue(path, f"marketplace policy must be {expected_policy}"))
    if not entry.get("category"):
        issues.append(ValidationIssue(path, "marketplace category is missing"))
    return issues


def validate_repository(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    required = [
        root / "AGENTS.md",
        root / "README.md",
        root / "LICENSE",
        root / "plugin.json",
        root / ".codex-plugin" / "plugin.json",
        root / ".agents" / "plugins" / "marketplace.json",
    ]
    for path in required:
        if not path.is_file():
            issues.append(ValidationIssue(path, "required file is missing"))

    if issues:
        return issues

    try:
        codex = load_json(root / ".codex-plugin" / "plugin.json")
        agent_plugin = load_json(root / "plugin.json")
    except (ValueError, json.JSONDecodeError) as error:
        issues.append(ValidationIssue(root, str(error)))
        return issues

    if codex.get("name") != agent_plugin.get("name"):
        issues.append(ValidationIssue(root, "Agent Plugin and Codex plugin names differ"))
    if codex.get("version") != agent_plugin.get("version"):
        issues.append(ValidationIssue(root, "Agent Plugin and Codex plugin versions differ"))
    if codex.get("skills") != "./skills/":
        issues.append(ValidationIssue(root, "Codex manifest must expose ./skills/"))
    if agent_plugin.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        issues.append(ValidationIssue(root / "plugin.json", "Agent Plugin schema is missing or unsupported"))
    plugin_name = codex.get("name")
    plugin_version = codex.get("version")
    if isinstance(plugin_name, str) and isinstance(plugin_version, str):
        issues.extend(
            validate_marketplace(
                root / ".agents" / "plugins" / "marketplace.json",
                plugin_name,
                plugin_version,
            )
        )

    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        issues.append(ValidationIssue(root / "skills", "no skills found"))
    for skill_path in skills:
        try:
            metadata = parse_frontmatter(skill_path)
        except ValueError as error:
            issues.append(ValidationIssue(skill_path, str(error)))
            continue
        expected_name = skill_path.parent.name
        if metadata.get("name") != expected_name:
            issues.append(ValidationIssue(skill_path, f"skill name must be {expected_name}"))
        if not metadata.get("description"):
            issues.append(ValidationIssue(skill_path, "skill description is missing"))
        openai_path = skill_path.parent / "agents" / "openai.yaml"
        if not openai_path.is_file():
            issues.append(ValidationIssue(openai_path, "skill UI metadata is missing"))
        else:
            openai_text = openai_path.read_text(encoding="utf-8")
            if f"${expected_name}" not in openai_text:
                issues.append(ValidationIssue(openai_path, "default prompt must mention the skill"))
        scripts_path = skill_path.parent / "scripts"
        if scripts_path.is_dir():
            for script_path in scripts_path.iterdir():
                if script_path.is_file() and script_path.stat().st_mode & 0o111 == 0:
                    issues.append(ValidationIssue(script_path, "skill script must be executable"))

    agents = sorted((root / "agents").glob("*.md"))
    if not agents:
        issues.append(ValidationIssue(root / "agents", "no agents found"))
    for agent_path in agents:
        try:
            metadata = parse_frontmatter(agent_path)
        except ValueError as error:
            issues.append(ValidationIssue(agent_path, str(error)))
            continue
        if not metadata.get("name") or not metadata.get("description"):
            issues.append(ValidationIssue(agent_path, "agent name or description is missing"))
        for reference in find_repository_references(agent_path, root):
            if not reference.is_file():
                issues.append(ValidationIssue(agent_path, f"repository reference is missing: {reference}"))

    automations = sorted((root / "automations").glob("*/FOR_AGENTS.md"))
    if not automations:
        issues.append(ValidationIssue(root / "automations", "no automation packs found"))
    for automation_path in automations:
        prompt_path = automation_path.parent / "prompt.md"
        if not prompt_path.is_file() or not prompt_path.read_text(encoding="utf-8").strip():
            issues.append(ValidationIssue(prompt_path, "automation prompt is missing or empty"))

    for markdown_path in sorted(path for path in repository_files(root) if path.suffix == ".md"):
        for link in find_local_markdown_links(markdown_path):
            if not link.is_file():
                issues.append(ValidationIssue(markdown_path, f"linked local resource is missing: {link}"))

    for placeholder_path in find_scaffold_placeholders(root):
        issues.append(ValidationIssue(placeholder_path, "unfinished scaffold placeholder"))

    return issues


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    issues = validate_repository(root)
    if issues:
        for issue in issues:
            print(f"{issue.path}: {issue.message}", file=sys.stderr)
        return 1
    skill_count = len(list((root / "skills").glob("*/SKILL.md")))
    agent_count = len(list((root / "agents").glob("*.md")))
    automation_count = len(list((root / "automations").glob("*/FOR_AGENTS.md")))
    print(f"Validated hoyelam-stack: {skill_count} skills, {agent_count} agents, {automation_count} automation packs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
