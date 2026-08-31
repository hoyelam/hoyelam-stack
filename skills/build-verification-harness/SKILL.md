---
name: build-verification-harness
description: Create and prove a project-local control skill, feature map, and evidence path when a repository lacks reliable real-application verification.
---

# Build Verification Harness

## Discover

1. Interview the repository before asking the user: identify the user-facing surfaces, supported launch commands, environment requirements, existing test drivers, observability, and isolation constraints.
2. Prefer an existing repository harness. Extend it only where the requested behavior cannot be proved.
3. Refuse to double-drive shared state when instances cannot be isolated safely.
4. For Apple applications, use `$verify-apple-apps` as the platform contract. For Electron applications, use `$verify-electron-apps`.
5. Read [references/harness-contract.md](references/harness-contract.md) before generating or substantially extending a harness.

## Build

1. Follow the repository's local skill convention. Create a project-local `verify-<app>` skill whose instructions are usable by an agent arriving without prior task context.
2. Add a small control CLI when repeated launch, drive, inspection, evidence, or cleanup commands would otherwise be improvised. Keep the CLI composable, machine-readable, self-documenting, and explicit about recovery.
3. Document the exact runtime and dependency versions, build-time network or cache assumptions, launch command, readiness signal, read-only doctor check, instance-isolation model, fixtures or authentication assumptions, supported interactions, evidence locations, and teardown procedure.
4. Use stable selectors, commands, routes, accessibility identifiers, or protocol inputs instead of screen coordinates when the platform permits it. For rendered web surfaces, prefer a live-proven role-and-name locator over source-only selector assumptions.
5. Exercise the real user path. Test-only setters and internal endpoints are not substitutes unless they are the production boundary being verified.
6. Capture the action and resulting state. Verify side effects through independent evidence such as files, database values, logs, responses, process health, or crash reports.
7. Kill only processes started by the harness. Preserve evidence while removing scratch state.

## Feature map

Create an indexed feature map with one file per behavior-level feature. Seed the three to five most important user-facing features, or every feature when the product is smaller. Each entry names:

1. Its stable feature identifier and sub-features.
2. How a user reaches every relevant entry point.
3. The exact harness commands that drive it.
4. The observable end state and side effects that prove it works.
5. Relevant permissions, fixtures, variants, timing, isolation, or cleanup risks.

## Prove the harness

1. Run `python3 <this-skill>/scripts/validate_harness.py <project-verification-skill>` before the live pass.
2. Run setup or launch, doctor, one mapped feature, evidence capture, and cleanup end to end.
3. Confirm the control CLI returns the documented machine-readable result, the feature proof identifies the artifact and harness revisions, and evidence survives cleanup.
4. Fix harness failures and rerun the affected path. Report product failures without changing product behavior unless that work is separately in scope.
5. A harness that has not driven the real artifact successfully is a draft, not completed verification infrastructure.
6. Route later drift audits and full feature-map sweeps through `$maintain-verification-harness` when it is available.
