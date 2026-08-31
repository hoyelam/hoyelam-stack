---
name: prove-the-work
description: Select the strongest relevant automated, build, and runtime evidence available to verify a code change proportionately to its behavior and risk.
---

# Prove The Work

## Verification ladder

1. Define the exact behavior, regression, or invariant being proved.
2. Inventory the repository's existing tests, static checks, build paths, runtime harnesses, feature maps, observability, available skills, and environment limits.
3. Select the layers that can catch realistic failures for this change. Route applicable iOS and macOS behavior through `$verify-apple-apps` and applicable Electron behavior through `$verify-electron-apps`.
4. Prefer focused unit tests for changed behavioral code when the owning boundary can be exercised meaningfully.
5. For a bug, make the test fail for the original reason when a cheap deterministic path exists.
6. Use snapshot tests only when pixels, layout, formatting, or rendered structure are the contract.
7. Run focused tests and add broader suites, linters, static checks, builds, or packaging when they cover material integration or release risk.
8. Rebuild and restart the real artifact when stale binaries or cached state could hide the result.
9. Exercise the user path with the project-local verification skill, computer use, or a deterministic script when the behavior has a meaningful runtime surface and the environment supports it. Identify mapped features and repeat timing-sensitive or crash-prone paths enough to challenge the original failure.
10. Inspect direct evidence such as UI state, process liveness, logs, persisted values, network results, generated artifacts, crash reports, or traces when relevant.
11. Add a nearby blast-radius check when adjacent behavior is plausibly affected, and prove the key safety fact as far as practical.
12. Rerun selected verification affected by review fixes.

## Evidence standard

Compilation proves syntax and linkage. Unit tests prove modeled behavior. Runtime checks prove only the paths actually exercised. Claim completion according to the strongest practical evidence available for the task, and name what remains unproved.

If a useful layer is irrelevant, unavailable, blocked, or disproportionate, state why, what was verified instead, and any remaining concrete risk. Do not rename proxy evidence as a stronger pass.
