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

Inspect the configured pull request's current diff, checks, review feedback, and repository instructions. Diagnose failures from actual logs and validate feedback against the current head. Wait when checks are running and no useful independent work is available.

Apply supported in-scope fixes on the existing branch. Follow `$hoyelam-mode` for proportional verification, useful delegation, review, and final-state evidence. Select checks that address the affected behavior while preserving repository and user requirements. Push only with configured authority and passing required local checks. Report the new head, checks actually observed, resolved findings, and blockers.

## Boundary

1. Do not approve, merge, deploy, release, dismiss human feedback, or create a competing pull request.
2. Do not rewrite history unless the user explicitly configured that authority.
3. Do not repeatedly post unchanged external status.
