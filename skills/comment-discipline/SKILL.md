---
name: comment-discipline
description: Audit comments and directives in a requested diff, preserving useful constraints.
---

# Comment Discipline

Prefer clear code, names, types, tests, and runtime checks over explanatory narration. Keep legal and license headers, required tool directives, and comments that explain a useful non-obvious constraint or public contract. Use the repository's conventions; no special prefix or metadata template is required by this skill.

Review the requested files or scoped diff, including the working tree. Read enough surrounding code and relevant evidence to understand a comment before changing it. Remove repetition, section banners, commented-out code, stale tasks, and explanations of avoidable complexity. Improve code instead when a small in-scope change makes the explanation unnecessary.

Judge comments by the information they preserve, not their prefix. A constraint comment should explain why the code must behave this way; add a source or removal condition when that helps future decisions. Check the purpose and effect of suppressions and directives before removal, and preserve their required syntax.

When edits are authorized, resolve supported findings and rerun affected checks. For a read-only audit, report findings without edits. Keep the report focused on meaningful changes, useful retained constraints, and any remaining verification gaps.
