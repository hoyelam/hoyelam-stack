#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath


FEATURE_HEADINGS = [
    "## Sub-features",
    "## User path",
    "## Harness drive",
    "## Proof",
    "## Gotchas",
]
SAFE_FEATURE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def issue(path: Path, message: str) -> dict[str, str]:
    return {"path": str(path), "message": message}


def validate(root: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    skill_path = root / "SKILL.md"
    features_path = root / "references" / "features"
    index_path = features_path / "README.md"

    if not skill_path.is_file():
        issues.append(issue(skill_path, "project verification skill is missing SKILL.md"))
    else:
        text = skill_path.read_text(encoding="utf-8")
        boundary = text.find("\n---\n", 4) if text.startswith("---\n") else -1
        frontmatter = text[4:boundary] if boundary >= 0 else ""
        name = re.search(r"^name:\s*([^\n]+)$", frontmatter, re.MULTILINE)
        if name is None or not name.group(1).strip().strip("\"'").startswith("verify-"):
            issues.append(issue(skill_path, "skill name must start with verify-"))

    if not index_path.is_file():
        issues.append(issue(index_path, "feature map index is missing"))
        return issues

    index = index_path.read_text(encoding="utf-8")
    linked: list[str] = []
    for target in re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", index):
        candidate = PurePosixPath(target)
        if candidate.is_absolute() or candidate.parent != PurePosixPath("."):
            issues.append(issue(index_path, f"feature link must target a sibling Markdown file: {target}"))
            continue
        linked.append(candidate.name)

    duplicates = sorted(name for name in set(linked) if linked.count(name) > 1)
    for name in duplicates:
        issues.append(issue(index_path, f"feature is indexed more than once: {name}"))

    feature_files = sorted(path for path in features_path.glob("*.md") if path.name != "README.md")
    for path in feature_files:
        if not SAFE_FEATURE.fullmatch(path.name):
            issues.append(issue(path, "feature filename must be a kebab-case identifier"))
        if path.name not in linked:
            issues.append(issue(path, "feature file is not linked from README.md"))
        text = path.read_text(encoding="utf-8")
        positions = [text.find(heading) for heading in FEATURE_HEADINGS]
        missing = [heading for heading, position in zip(FEATURE_HEADINGS, positions) if position == -1]
        for heading in missing:
            issues.append(issue(path, f"missing required heading: {heading}"))
        present = [position for position in positions if position >= 0]
        if present != sorted(present):
            issues.append(issue(path, "required feature headings are out of order"))

    known = {path.name for path in feature_files}
    for name in sorted(set(linked) - known):
        issues.append(issue(index_path, f"indexed feature file is missing: {name}"))
    if not feature_files:
        issues.append(issue(features_path, "feature map must contain at least one feature file"))

    scripts_path = root / "scripts"
    if scripts_path.is_dir():
        for path in sorted(item for item in scripts_path.iterdir() if item.is_file()):
            if path.stat().st_mode & 0o111 == 0:
                issues.append(issue(path, "harness script must be executable"))
    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"ok": False, "error": "usage: validate_harness.py <project-verification-skill>"}))
        return 2
    root = Path(sys.argv[1]).resolve()
    issues = validate(root)
    print(json.dumps({"ok": not issues, "skill": str(root), "issues": issues}, indent=2, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
