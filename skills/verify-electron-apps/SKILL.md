---
name: verify-electron-apps
description: Verify Electron process boundaries and affected renderer or native behavior.
---

# Verify Electron Apps

Select checks for the affected Electron behavior and keep user-requested and repository-required checks as completion gates. Consult `$prove-the-work` when acceptance checks or the strength of the evidence need clarification.

## Route the work

1. Use project verification commands and relevant tests for the changed boundary. Inspect launch harnesses for runtime proof, and Electron version or packaging configuration when compatibility or distribution affects the claim.
2. Map the changed behavior to the owning process: main, preload, renderer, utility process, worker, or native operating-system surface.
3. Read [references/electron-verification.md](references/electron-verification.md) before launching or driving the application.
4. Use repository-owned unit, integration, Playwright, or equivalent end-to-end infrastructure when it proves the claim. This skill bundles a CDP readiness diagnostic and protocol guidance; desktop computer use, Playwright, and other runtime tools depend on the environment. Check actual availability before depending on them. Add a harness only when a required proof is missing and setup is within scope.

## Verification contract

1. Define the exact invariant, original failure path, process boundary, nearby regression path, and observable evidence.
2. Use focused unit or integration coverage at the lowest layer that owns the behavior; add coverage when it materially tests a changed contract. Test IPC contracts from both sides when their schema or lifecycle changed.
3. Run focused tests and select broader suites, type checks, linting, and packaged or distributable builds according to process-boundary, integration, packaging, and release risk.
4. When runtime behavior needs direct evidence, launch the current artifact with an isolated test profile. If debugging ports are used, bind them to loopback. Never attach verification tooling to the user's normal application profile.
5. Use an existing project harness, Chrome DevTools Protocol, Playwright Electron, computer use, or an equivalent deterministic path that can prove the runtime claim. Renderer proof does not inherently require CDP or Playwright. Use the main-process V8 inspector when that inspection is needed; a main-process change alone does not require an inspector session.
6. Capture the console, exception, request, target, DOM or accessibility, screenshot, process, and persisted-side-effect evidence relevant to the selected proof.
7. During runtime verification, prefer DOM, accessibility, roles, labels, or stable test identifiers for renderer interaction. Use computer use or an equivalent native harness for relevant surfaces outside Chromium's DOM.
8. Rebuild and relaunch after edits when stale artifacts could hide the result. Confirm any connected DevTools target belongs to the newly launched artifact.
9. Repeat race-prone, reload, sleep/wake, close/reopen, multi-window, IPC, and crash paths when they are in scope.
10. Test development and packaged behavior when bundling, paths, protocols, updates, native modules, signing, preload loading, or content security differs between them.
11. Rerun selected layers affected by every verified review fix.

## Optional CDP readiness diagnostic

When CDP is selected and readiness or target identity needs diagnosis, launch the app through its supported verification command and run `python3 <skill-root>/scripts/electron_cdp_doctor.py --renderer-port <port> --expected-title <title> --expected-url <url-fragment>`. Add `--main-port <port> --require-main` only when both renderer and main-process inspection are part of the proof. The doctor checks renderer targets and is unnecessary for a main-only check, a harness that already establishes readiness and identity, or a proof that does not use CDP, unless the project or user requires it. It verifies protocol reachability and identity, never application behavior.

## Completion evidence

Return the commands, test results and counts, tested state or artifact, and observations relevant to the selected proof. Include profile and process identities for runtime runs, target identity when using DevTools, and packaging, screenshots, network, persistence, repetition, or cleanup evidence where relevant. A pure logic or documentation change does not automatically require packaging, desktop interaction, debugging ports, or a doctor run. Failed or blocked required checks leave verification incomplete; name material optional omissions without calling them passes.
