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
3. Run the focused tests, full relevant suite, type checks, linting, and a production-representative packaged or distributable build.
4. Launch the current artifact with an isolated test profile and loopback-only debugging ports. Never attach verification tooling to the user's normal application profile.
5. Verify renderer targets through the Chrome DevTools Protocol or the repository's Playwright Electron harness. Verify the main process separately through the V8 inspector when main-process behavior changed.
6. Capture console errors, uncaught exceptions, failed requests, target crashes, DOM or accessibility state, screenshots, network evidence, process health, and persisted side effects.
7. Use DOM, accessibility, roles, labels, or stable test identifiers for renderer interaction. Use computer use for native menus, dialogs, tray items, window chrome, drag and drop, permission sheets, and behavior outside Chromium's DOM.
8. Rebuild and relaunch after edits. Confirm the connected DevTools target belongs to the newly launched artifact.
9. Repeat race-prone, reload, sleep/wake, close/reopen, multi-window, IPC, and crash paths enough to challenge the original failure.
10. Test development and packaged behavior when bundling, paths, protocols, updates, native modules, signing, preload loading, or content security differs between them.
11. Rerun affected layers after every verified review fix.

## Doctor

Launch the app through its supported verification command, then run `python3 <skill-root>/scripts/electron_cdp_doctor.py --renderer-port <port> --expected-title <title> --expected-url <url-fragment>`. Add `--main-port <port> --require-main` when main-process inspection is part of the proof. The doctor verifies reachable protocol targets and identity; it does not prove application behavior.

## Completion evidence

Return the commands, test results, packaged artifact, isolated-profile path, process identities, DevTools endpoints and target identity, interaction path, DOM or accessibility assertions, screenshots, console and network findings, persisted side effects, repetition count, blast-radius check, cleanup result, and every blocked layer.
