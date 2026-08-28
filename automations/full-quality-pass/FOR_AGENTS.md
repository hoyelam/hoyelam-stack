# Full quality pass automation

## Intent

Finish an already-implemented branch through tests, real behavior verification, comment audit, extensive review, finding resolution, and a final evidence report.

## Required configuration

1. Repository path and expected branch.
2. Base branch.
3. Repository verification commands.
4. Real artifact launch or control path.
5. User behavior or regression to verify.

## Execution

1. Read the repository `AGENTS.md` and `skills/hoyelam-mode/SKILL.md`.
2. Confirm the repository, branch, base, worktree scope, and user-requested behavior.
3. Stop on unrelated destructive state or ambiguous ownership.
4. Run unit tests, the full relevant suite, static checks, and a production-representative build.
5. Run the real behavior through computer use or a deterministic verification script.
6. Run the comment auditor and code reviewer on the complete scoped diff.
7. Verify each finding before editing.
8. Resolve every verified in-scope finding.
9. Repeat affected tests, build, runtime verification, comment audit, and code review until clean.
10. Update only the existing branch. Do not create a second competing pull request.

## Boundary

1. Do not merge, deploy, release, or broaden scope.
2. Do not hide failed or blocked verification.
3. Do not treat a reviewer report as evidence that the real behavior works.
