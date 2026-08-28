# Platform verification

## Apple applications

1. Invoke `$verify-apple-apps` for iOS and macOS behavioral changes.
2. Use the focused automated layer that owns the behavior, then the full relevant test plan or suite.
3. Build and launch the real application artifact.
4. Verify iOS through XCUITest, Maestro, Simulator control, computer use, or a repository harness.
5. Verify macOS through application tests, computer use, logs, process state, signing, entitlements, and direct system side effects.
6. Preserve `.xcresult`, screenshot, log, crash, persistence, and artifact evidence relevant to the change.

## Electron applications

1. Invoke `$verify-electron-apps` for Electron behavioral changes.
2. Identify whether main, preload, renderer, utility, or native operating-system behavior owns the change.
3. Run focused and full tests, type checks, linting, and a packaged build.
4. Launch with an isolated profile and loopback-only DevTools endpoints.
5. Use Chrome DevTools Protocol or the repository's Playwright Electron harness for Chromium surfaces.
6. Use computer use for native menus, dialogs, tray items, permissions, window chrome, and drag and drop.
7. Preserve console, exception, network, target, DOM, accessibility, screenshot, process, persistence, and packaged-artifact evidence.

## Shared completion rule

1. Environment readiness is not behavior verification.
2. Compilation and unit tests alone are not end-to-end proof.
3. A screenshot without the action, state transition, and side-effect evidence is incomplete.
4. Every verified review fix returns through the affected automated and runtime layers.
5. Blocked layers remain named and cannot be relabeled as passing.

## Agent use

1. The two platform skills are installed directly and are the stable invocation surface in Codex.
2. `agents/apple-runtime-verifier.md` and `agents/electron-runtime-verifier.md` are portable specialist specifications, not separately registered Codex agent names.
3. When delegation is available and authorized, give a verification worker the relevant agent file and require it to read the referenced platform skill in full.
4. Without delegation, the primary agent follows the same specification directly.
