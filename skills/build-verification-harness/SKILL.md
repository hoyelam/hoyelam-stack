---
name: build-verification-harness
description: Create a project-local, repeatable way to launch, drive, observe, and clean up the real application when a repository lacks reliable behavior verification.
---

# Build Verification Harness

## Discover

1. Interview the repository before asking the user: identify the user-facing surfaces, supported launch commands, environment requirements, existing test drivers, observability, and isolation constraints.
2. Prefer an existing repository harness. Extend it only where the requested behavior cannot be proved.
3. Refuse to double-drive shared state when instances cannot be isolated safely.
4. For Apple applications, use `$verify-apple-apps` as the platform contract. For Electron applications, use `$verify-electron-apps`.

## Build

1. Follow the repository's local skill convention. Prefer a project-local `verify-<app>` skill plus deterministic helper scripts when repeated commands would otherwise be improvised.
2. Document the exact launch command, readiness signal, read-only doctor check, supported interactions, evidence locations, and teardown procedure.
3. Use stable selectors, commands, routes, accessibility identifiers, or protocol inputs instead of screen coordinates when the platform permits it.
4. Exercise the real user path. Test-only setters and internal endpoints are not substitutes unless they are the production boundary being verified.
5. Capture the action and resulting state. Verify side effects through independent evidence such as files, database values, logs, responses, process health, or crash reports.
6. Kill only processes started by the harness. Preserve evidence while removing scratch state.

## Feature map

Seed a small map of the main user-facing behaviors. Each entry names:

1. What the user can do.
2. How the user reaches it.
3. How the harness drives it.
4. What observable end state proves it works.
5. Relevant permissions, fixtures, timing, or cleanup risks.

## Prove the harness

Run launch, doctor, one mapped feature, evidence capture, and cleanup end to end. Confirm evidence survives cleanup. A harness that has not driven the real artifact successfully is a draft, not completed verification infrastructure.
