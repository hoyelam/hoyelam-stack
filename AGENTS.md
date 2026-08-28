# hoyelam-stack working agreement

## Preferred engineering workflow

Treat this workflow as a decision aid, not a mandatory sequence. First inspect the request, repository instructions, task risk, existing tests, supported build paths, runtime surfaces, and available tools and skills. Select, combine, reorder, or omit workflow layers according to what can materially prove the requested outcome.

1. Reconstruct relevant prior context when resuming older work, then reconcile it with live repository state.
2. Investigate enough to distinguish the request, expected behavior, origin, and smallest meaningful boundary before editing.
3. Locate the actual repository, applicable instructions, owning source, callers, tests, history, and adjacent behavior that matter to the change.
4. Read relevant architecture documentation and platform skills when they can change the implementation decision.
5. Fix the root cause with the smallest complete change that fits the existing architecture.
6. Prefer unit coverage for behavioral code. Use snapshot tests only when rendered output or visual structure is the behavior under test.
7. Choose focused checks, broader suites, static analysis, builds, and runtime interaction according to the failure modes they can catch.
8. Exercise the real behavior with computer use or a deterministic script when the change has a meaningful runtime surface and the environment supports it.
9. Use `verify-apple-apps` for relevant iOS and macOS verification and `verify-electron-apps` for relevant Electron verification.
10. Scale comment, correctness, simplicity, architecture, and test-quality review to the diff and its risk.
11. Resolve every verified in-scope finding, then rerun the affected selected verification.
12. When interrupted, preserve recoverable work and a precise resume capsule without claiming completion.
13. Use `orchestrate-project` only for independently executable work that spans units or sessions; collapse to direct work when one agent can reasonably finish it.

## Hard boundaries

1. Preserve the user's scope and authorization limits.
2. Treat a workflow or verification layer explicitly requested by the user as required unless it is genuinely blocked.
3. Follow closer repository instructions when they conflict with a general preference here.
4. Never report an omitted, unavailable, or blocked verification layer as passing.
5. Increase verification depth for security, privacy, data loss, money, permissions, signing, concurrency, migration, and release risk.
6. Resolve verified in-scope findings before claiming completion.
7. Do not perform destructive or external actions without the required authority.

## Comments

1. Prefer code, types, names, tests, runtime checks, and tooling over comments.
2. Keep legal and license headers.
3. Keep a comment only for a proven external constraint that cannot be made obvious or executable.
4. Prefix rare constraint comments with exactly one of `IMPORTANT`, `DO NOT REMOVE`, `TOO RISKY`, or `FINE FOR NOW`.
5. Every prefixed comment must name the external constraint, evidence source, failure mode, and removal condition when one exists.
6. Treat the prefix as a review trigger, not proof that the comment deserves to remain.
7. Remove narration, section banners, commented-out code, workaround stories, stale TODOs, and comments that repeat the code.
