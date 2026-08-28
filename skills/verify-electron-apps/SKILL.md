---
name: verify-electron-apps
description: Verify Electron changes across main, preload, renderer, and native surfaces with automated tests, packaged builds, Chrome DevTools Protocol evidence, and real desktop interaction.
---

# Verify Electron Apps

Apply `$prove-the-work`. This skill specializes its verification ladder for Electron applications.

## Route the work

1. Read repository instructions, package scripts, Electron version, builder or packager configuration, test frameworks, and existing launch harnesses.
2. Map the changed behavior to the owning process: main, preload, renderer, utility process, worker, or native operating-system surface.
3. Read [references/electron-verification.md](references/electron-verification.md) before launching or driving the application.
4. Prefer repository-owned unit, integration, Playwright, Spectron replacement, or end-to-end infrastructure. Add a new harness only when the current project cannot prove the requested behavior.

## Verification contract

1. Define the exact invariant, original failure path, process boundary, nearby regression path, and observable evidence.
2. Add focused unit or integration coverage at the lowest layer that owns the behavior. Test IPC contracts from both sides when their schema or lifecycle changed.
3. Run focused tests and select broader suites, type checks, linting, and packaged or distributable builds according to process-boundary, integration, packaging, and release risk.
4. When runtime behavior needs direct evidence, launch the current artifact with an isolated test profile and loopback-only debugging ports. Never attach verification tooling to the user's normal application profile.
5. When renderer runtime verification is selected, use the Chrome DevTools Protocol or the repository's Playwright Electron harness. Inspect the main process separately through the V8 inspector only when main-process behavior changed.
6. Capture the console, exception, request, target, DOM or accessibility, screenshot, process, and persisted-side-effect evidence relevant to the selected proof.
7. During runtime verification, use DOM, accessibility, roles, labels, or stable test identifiers for renderer interaction. Use computer use for relevant native surfaces outside Chromium's DOM.
8. Rebuild and relaunch after edits when stale artifacts could hide the result. Confirm any connected DevTools target belongs to the newly launched artifact.
9. Repeat race-prone, reload, sleep/wake, close/reopen, multi-window, IPC, and crash paths when they are in scope.
10. Test development and packaged behavior when bundling, paths, protocols, updates, native modules, signing, preload loading, or content security differs between them.
11. Rerun selected layers affected by every verified review fix.

## Doctor

Launch the app through its supported verification command, then run `python3 <skill-root>/scripts/electron_cdp_doctor.py --renderer-port <port> --expected-title <title> --expected-url <url-fragment>`. Add `--main-port <port> --require-main` when main-process inspection is part of the proof. The doctor verifies reachable protocol targets and identity; it does not prove application behavior.

## Completion evidence

Return the commands, test results, packaged artifact, isolated-profile path, process identities, DevTools endpoints and target identity, interaction path, DOM or accessibility assertions, screenshots, console and network findings, persisted side effects, repetition count, blast-radius check, cleanup result, and every blocked layer.
