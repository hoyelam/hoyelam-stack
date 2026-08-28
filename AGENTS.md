# hoyelam-stack working agreement

## Output

1. Apply the `i-have-adhd` skill on every turn.
2. Lead with the current state or next action.
3. Use numbered steps, no preamble, and no closing filler.
4. Restate the task state on every turn.

## Engineering workflow

1. Reconstruct relevant prior context before resuming older work, then reconcile it with live repository state.
2. Investigate the request, observable symptom, expected behavior, origin, and evidence before editing.
3. Locate the actual repository, applicable instructions, source, callers, tests, history, and adjacent behavior.
4. Isolate the feature or defect at the smallest meaningful boundary.
5. Read the repository's architecture documentation and use relevant platform skills before implementation.
6. Fix the root cause with the smallest complete change that fits the existing architecture.
7. Add or update unit tests for every behavioral change. Add snapshot tests only when rendered output or visual structure is the behavior under test.
8. Run focused checks, the full relevant suite, and a production-representative build.
9. Manually exercise the behavior with computer use or a deterministic script and inspect runtime evidence. Build a reusable project-local harness when that path would otherwise be rediscovered.
10. Use `verify-apple-apps` for iOS and macOS behavior and `verify-electron-apps` for Electron behavior.
11. Run comment, correctness, simplicity, architecture, and test-quality review passes.
12. Resolve every verified in-scope finding, then rerun affected verification.
13. When interrupted, preserve recoverable work and a precise resume capsule without claiming completion.

## Comments

1. Prefer code, types, names, tests, runtime checks, and tooling over comments.
2. Keep legal and license headers.
3. Keep a comment only for a proven external constraint that cannot be made obvious or executable.
4. Prefix rare constraint comments with exactly one of `IMPORTANT`, `DO NOT REMOVE`, `TOO RISKY`, or `FINE FOR NOW`.
5. Every prefixed comment must name the external constraint, evidence source, failure mode, and removal condition when one exists.
6. Treat the prefix as a review trigger, not proof that the comment deserves to remain.
7. Remove narration, section banners, commented-out code, workaround stories, stale TODOs, and comments that repeat the code.

## GitHub CLI

1. Use `gh` for GitHub operations.
2. Before the first authenticated GitHub operation, run `gh auth status --hostname github.com` and `gh api user --jq .login`.
3. Retry sandbox-related keychain, network, DNS, or permission failures with required elevated permission before judging authentication.
4. Before repository writes, verify `gh api repos/OWNER/REPO --jq '.permissions.push'`.
5. Never print, inspect, copy, or persist token values.
6. If authentication is invalid, stop GitHub mutations and ask the user to authenticate in their own terminal.
