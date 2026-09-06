---
name: build-verification-harness
description: Create or extend a repeatable project verification path when a repository lacks reliable real-application verification.
---

# Build Verification Harness

## Discover

1. Interview the repository before asking the user: identify the user-facing surfaces, supported launch commands, environment requirements, existing test drivers, observability, and isolation constraints.
2. Prefer an existing repository harness. Extend it only where the requested behavior cannot be proved.
3. Refuse to double-drive shared state when instances cannot be isolated safely.
4. For iOS applications, use `$verify-ios-apps`; for macOS use `$verify-macos-apps`. For Electron applications, use `$verify-electron-apps`.
5. Keep a working repository harness and its conventions. Use the [bundled harness template](references/harness-contract.md) when creating a `verify-<app>` skill; its directory layout and validator apply only to that format.

## Build

1. Make setup, supported interactions, expected outcomes, evidence capture, and cleanup discoverable to an agent arriving without prior context. Extend existing scripts, test drivers, and docs where sufficient. If no suitable convention exists, create a project-local `verify-<app>` skill using the bundled template.
2. Add a small control CLI when repeated launch, drive, inspection, evidence, or cleanup commands would otherwise be improvised. Keep the CLI composable, machine-readable, self-documenting, and explicit about recovery.
3. Document the exact runtime and dependency versions, build-time network or cache assumptions, launch command, readiness signal, read-only readiness and instance-identity check, instance-isolation model, fixtures or authentication assumptions, supported interactions, evidence locations, and teardown procedure.
4. Use stable selectors, commands, routes, accessibility identifiers, or protocol inputs instead of screen coordinates when the platform permits it. For rendered web surfaces, prefer a live-proven role-and-name locator over source-only selector assumptions.
5. Exercise the real user path. Test-only setters and internal endpoints are not substitutes unless they are the production boundary being verified.
6. Capture the action and resulting state. Verify side effects through independent evidence such as files, database values, logs, responses, process health, or crash reports.
7. Kill only processes started by the harness. Preserve evidence while removing scratch state.

## Feature map

Map the behavior needed for the requested verification. Reuse existing scenarios, test catalogs, or documentation; separate feature files are a bundled template convention. Expand coverage when requested or when repeated verification needs it. Each mapped behavior names:

1. Its stable feature identifier and sub-features.
2. How a user reaches every relevant entry point.
3. The exact harness commands that drive it.
4. The observable end state and side effects that prove it works.
5. Relevant permissions, fixtures, variants, timing, isolation, or cleanup risks.

## Prove the harness

1. Validate using the project’s supported checks. For the bundled skill format, also run `python3 <this-skill>/scripts/validate_harness.py <project-verification-skill>` before the live pass.
2. Run setup or launch, readiness and identity checks, one scoped user behavior, evidence capture, and cleanup end to end through the chosen control path.
3. Confirm commands return their documented results, behavior evidence identifies the artifact and harness revisions, and evidence survives cleanup. Use machine-readable output where another tool consumes it; the bundled CLI template uses JSON.
4. Fix harness failures and rerun the affected path. Report product failures without changing product behavior unless that work is separately in scope.
5. A harness that has not driven the real artifact successfully is a draft, not completed verification infrastructure.
6. Route later drift audits of the bundled skill and feature-map format through `$maintain-verification-harness`; maintain existing harness formats with their own checks and the same evidence standard.
