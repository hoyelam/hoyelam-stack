---
name: prove-the-work
description: Verify a code change with mandatory unit coverage, the full relevant suite, a production-representative build, and direct runtime evidence from computer use or a deterministic script.
---

# Prove The Work

## Verification ladder

1. Define the exact behavior, regression, or invariant being proved.
2. Route iOS and macOS behavior through `$verify-apple-apps` and Electron behavior through `$verify-electron-apps`.
3. Add or update focused unit tests for every changed behavior.
4. For a bug, make the test fail for the original reason when a cheap deterministic path exists.
5. Use snapshot tests only when pixels, layout, formatting, or rendered structure are the contract.
6. Run focused tests and record exact counts or failures.
7. Run the full relevant suite, linters, static checks, and a production-representative build.
8. Rebuild and restart the real artifact when stale binaries or cached state could hide the result.
9. Exercise the user path with computer use or a deterministic script. Repeat timing-sensitive or crash-prone paths enough to challenge the original failure.
10. Inspect direct evidence such as UI state, process liveness, logs, persisted values, network results, generated artifacts, crash reports, or traces.
11. Run a nearby blast-radius smoke test and directly prove the key fact the change is safe because of.
12. Rerun affected verification after review fixes.

## Evidence standard

Compilation proves syntax and linkage. Unit tests prove modeled behavior. Neither proves the real application path. Claim completion only when the strongest practical evidence covers the user's exact behavior.

If manual verification is blocked, state the blocker, what was verified instead, and the remaining concrete check. Do not rename proxy evidence as a manual pass.
