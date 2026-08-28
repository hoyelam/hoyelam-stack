---
name: comment-discipline
description: Audit a scoped diff or set of files for unnecessary comments, prove rare exceptions, remove accepted comment findings, and encode constraints in executable form when practical.
---

# Comment Discipline

## Default

Comments are a last resort. Prefer clearer names, smaller functions, stronger types, explicit state, tests, runtime checks, and tooling.

## Allowed exceptions

1. Legal or license headers.
2. A non-obvious external platform, protocol, dependency, vendor, or compatibility constraint that cannot be made clear or executable in the code.
3. A required tool directive whose removal changes generated or formatted output.

Public documentation comments survive only when they define a contract that cannot be expressed by the declaration and are required by the repository's public API policy.

## Required prefixes

Rare non-legal comments use exactly one prefix:

1. `IMPORTANT` for a proven invariant imposed outside the code.
2. `DO NOT REMOVE` when removal causes a specific externally imposed failure.
3. `TOO RISKY` for a rejected alternative with current evidence of unacceptable risk.
4. `FINE FOR NOW` for a bounded temporary tradeoff with an owner, removal condition, or tracking reference.

A prefix starts investigation; it does not justify the comment. The text must identify the external constraint, evidence source, failure mode, and removal condition when one exists.

## Audit

1. Scope to caller-provided files or the current diff against the base branch, including the working tree.
2. Find line comments, block comments, documentation comments, disabled-code blocks, TODO variants, lint suppressions, formatter directives, and the four prefixes.
3. Read the surrounding symbol, callers, tests, and relevant history before judging a non-obvious comment.
4. Delete narration, banners, repetition, commented-out code, workaround stories, stale tasks, and comments explaining avoidable complexity.
5. Replace our-code surprises with clearer code, types, or structure in the smallest in-scope change.
6. Treat lint and compiler suppressions as findings unless the rule is proven faulty, style-only, or unavoidable at an external boundary.
7. Preserve an exception only with scoped evidence that is true today.
8. Offer a test, type, runtime assertion, generated check, or CI rule when it can replace a surviving constraint comment.
9. Rerun affected checks after changes.

## Report

Report reviewed files, deleted comments, rewritten code, preserved exceptions with evidence, encoded constraints, unresolved out-of-scope findings, and verification.
