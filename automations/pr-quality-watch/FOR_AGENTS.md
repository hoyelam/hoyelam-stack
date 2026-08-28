# Pull request quality watch automation

## Intent

Keep one configured pull request review-ready by diagnosing CI and review feedback, applying only verified in-scope fixes, and proving the updated head.

## Required configuration

1. Repository owner and name.
2. Pull request number or an unambiguous selection rule.
3. Repository verification commands.
4. Real artifact launch or control path when runtime behavior changed.

## GitHub gate

1. Use `gh` for every GitHub operation.
2. Before the first authenticated operation, run `gh auth status --hostname github.com` and `gh api user --jq .login`.
3. Before any repository write, verify `gh api repos/OWNER/REPO --jq '.permissions.push'`.
4. Stop mutations when authentication, repository identity, or push permission is invalid.

## Execution

1. Read repository instructions and the current pull request diff, checks, review threads, and recent commits.
2. Wait when checks are still running and no action is available.
3. Diagnose failures from their logs and reproduce locally when practical.
4. Verify review feedback against the current head before changing code.
5. Apply only verified in-scope fixes on the existing pull request branch.
6. Add or update unit tests for changed behavior.
7. Run focused checks, the full relevant suite, a production-representative build, and direct behavior verification when applicable.
8. Run comment and final code review passes before pushing.
9. Push only after the complete local quality pass succeeds.
10. Report the new head, checks, runtime evidence, resolved review threads, and remaining blockers.

## Boundary

1. Do not approve, merge, deploy, release, dismiss human feedback, or create a competing pull request.
2. Do not rewrite history unless the user explicitly configured that authority.
3. Do not repeatedly post unchanged external status.
