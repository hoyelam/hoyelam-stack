# Platform verification

## Apple applications

1. Invoke `$verify-apple-apps` for iOS and macOS behavioral changes.
2. Select focused tests, broader plans or suites, and builds according to the changed boundary and risk.
3. Build and launch the real application artifact when runtime, target, signing, entitlement, packaging, or integration behavior needs direct evidence.
4. For selected iOS runtime verification, use XCUITest, Maestro, Simulator control, computer use, or a repository harness.
5. For selected macOS runtime verification, use relevant application tests, computer use, logs, process state, signing, entitlements, and direct system side effects.
6. Preserve only the `.xcresult`, screenshot, log, crash, persistence, and artifact evidence relevant to the selected proof.

## Electron applications

1. Invoke `$verify-electron-apps` for Electron behavioral changes.
2. Identify whether main, preload, renderer, utility, or native operating-system behavior owns the change.
3. Select focused and broader tests, type checks, linting, and packaged builds according to process-boundary, integration, packaging, and release risk.
4. When runtime evidence is selected, launch with an isolated profile and loopback-only DevTools endpoints.
5. Use Chrome DevTools Protocol or the repository's Playwright Electron harness for relevant Chromium surfaces.
6. Use computer use for relevant native menus, dialogs, tray items, permissions, window chrome, and drag and drop.
7. Preserve only the console, exception, network, target, DOM, accessibility, screenshot, process, persistence, and packaged-artifact evidence relevant to the selected proof.

## Shared completion rule

1. Environment readiness is not behavior verification.
2. Compilation and unit tests alone are not end-to-end proof when the claim concerns real runtime behavior.
3. A screenshot without the action, state transition, and side-effect evidence is incomplete.
4. Every verified review fix returns through the affected selected automated and runtime layers.
5. Blocked layers remain named and cannot be relabeled as passing.
6. When a project-local verification skill exists, use its mapped feature identifier and preserve its structured evidence receipt with the platform evidence.

## Agent use

1. The two platform skills are installed directly and are the stable invocation surface in Codex.
2. `agents/apple-runtime-verifier.md` and `agents/electron-runtime-verifier.md` are portable specialist specifications, not separately registered Codex agent names.
3. When delegation is available and authorized, give a verification worker the relevant agent file and require it to read the referenced platform skill in full.
4. Without delegation, the primary agent follows the same specification directly.
