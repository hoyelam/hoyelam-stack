# Workflow

## State machine

1. `Recalling`: when work is resumed, reconcile relevant prior decisions with current repository state.
2. `Investigating`: establish expected behavior, symptom, origin, repository, evidence, and completion condition.
3. `Locating`: find owning source, callers, tests, history, architecture documents, and adjacent behavior.
4. `Isolating`: choose the smallest feature or defect boundary that can be changed and proved independently.
5. `Implementing`: fit the smallest complete root-cause solution into the existing architecture.
6. `Testing`: add mandatory unit coverage, then run focused and full automated checks.
7. `Verifying`: build the real artifact and exercise the exact behavior with computer use or a deterministic script.
8. `Reviewing`: audit comments, correctness, simplicity, architecture, lifecycle, tests, and user experience.
9. `Resolving`: fix every verified in-scope finding and return to testing and verification.
10. `Complete`: report direct evidence, remaining boundaries, and worktree state.
11. `Checkpointed`: when interrupted, preserve recoverable work and a precise resume capsule without claiming completion.

## Investigation standard

1. The working directory is a hint, not proof of repository ownership.
2. A stack trace is a starting point, not automatically the root cause.
3. History matters when the symptom is a regression or a deliberate compromise.
4. Runtime evidence outranks a plausible source-only explanation.
5. The implementation boundary should be named before edits begin.

## Implementation standard

1. Preserve established architecture and conventions.
2. Read authoritative documentation for external APIs and unstable platform behavior.
3. Make state and side effects testable.
4. Prefer deletion, direct modeling, and small boundaries over wrappers and compatibility layers.
5. Keep unrelated cleanup out of the change.

## Verification standard

1. Unit tests are mandatory for behavioral changes.
2. Snapshot tests are conditional on rendered output being the contract.
3. Focused tests provide fast diagnosis; the full suite catches integration regressions.
4. A production-representative build catches target, entitlement, linkage, and configuration failures.
5. Manual behavior evidence catches failures no unit test modeled.
6. Every review fix returns through the affected verification steps.
7. Repositories without a reliable real-app control path should gain a project-local verification harness rather than inventing a new manual recipe for every task.
8. iOS and macOS verification follows `$verify-apple-apps`; Electron verification follows `$verify-electron-apps`.

## Completion report

1. Root cause or satisfied requirement.
2. Owning boundary and implementation.
3. Unit and snapshot coverage.
4. Focused and full test results.
5. Build result and target.
6. Manual path and direct runtime evidence.
7. Verified review findings resolved.
8. Remaining external or out-of-scope work.
9. Branch, commit, and worktree state when relevant.
