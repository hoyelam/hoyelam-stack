# Full quality pass automation

## Intent

Apply the user's verification and review method to an already-implemented branch. This is an optional scheduled wrapper; the same work can run directly through `$hoyelam-mode`.

## Required configuration

1. Repository, expected branch, base, and writable scope.
2. Intended outcome and observable acceptance criteria, including any explicitly required checks.
3. Supported verification commands or evidence sources appropriate to the change.
4. For application runtime behavior, the launch or control path, fixtures, and user behavior to verify. Documentation-only work does not require an application launch path.

## Execution

1. Read the repository `AGENTS.md` and the installed `$hoyelam-mode` skill.
2. Confirm repository, branch, base, ownership, authorized fixes, and intended outcome.
3. Define the verification plan before fixing anything. Select checks that can disprove the acceptance criteria: source and link validation for documentation, focused tests for logic, broader suites or builds for integration risk, and real interactions for runtime behavior. Preserve explicitly required checks as gates.
4. Run the selected checks and record actual evidence. Missing required tools leave verification incomplete; optional omissions need a concrete reason.
5. Review the complete scoped diff through `$review-and-resolve`. Include comment review when relevant, and independent review for substantial or risky changes when available and authorized. A named specialist agent is not required for every change.
6. Validate findings before editing. Automatically resolve confirmed in-scope issues within the configured authority.
7. Rerun affected verification and inspect the revised diff. Continue until required evidence is current and no verified in-scope findings remain, or report the exact blocker.
8. Report the outcome and evidence. Update only the configured branch; do not create a competing pull request. Pushing or posting requires configured authority.

## Boundary

1. Do not merge, deploy, release, or broaden scope.
2. Never hide failed or blocked required verification or treat readiness as behavior proof.
3. A reviewer report alone does not establish that the intended behavior works.
