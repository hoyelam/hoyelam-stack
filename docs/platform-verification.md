# Platform verification

## iOS and macOS applications

1. Use [verify-ios-apps](../skills/verify-ios-apps/SKILL.md) for iOS and [verify-macos-apps](../skills/verify-macos-apps/SKILL.md) for macOS. [verify-apple-apps](../skills/verify-apple-apps/SKILL.md) remains the compatibility route for existing invocations and mixed-platform work. They share the Apple verification contract, references, and optional doctor.
2. Select focused tests, broader plans or suites, and builds according to the changed boundary and risk.
3. Build and launch the real application artifact when runtime, target, signing, entitlement, packaging, or integration behavior needs direct evidence.
4. For selected iOS runtime verification, use XCUITest, Maestro, XcodeBuildMCP or other Simulator control, computer use, or an equivalent repository harness. Swift Testing, XCTest, and package tests may suffice for logic claims.
5. For selected macOS runtime verification, use the supported Xcode or SwiftPM app build/run path, application tests, computer use or an equivalent native harness, logs, and process state. Check signing, entitlements, and system side effects when those boundaries matter. A library package check needs no Simulator or app launch.
6. Preserve only the `.xcresult`, screenshot, log, crash, persistence, and artifact evidence relevant to the selected proof.

## Electron applications

1. Invoke `$verify-electron-apps` for Electron behavioral changes.
2. Identify whether main, preload, renderer, utility, or native operating-system behavior owns the change.
3. Select focused and broader tests, type checks, linting, and packaged builds according to process-boundary, integration, packaging, and release risk.
4. When runtime evidence is selected, launch the current artifact with an isolated profile. Bind any debugging endpoints to loopback; a valid runtime proof need not open debugging ports.
5. Use a repository harness, Chrome DevTools Protocol, Playwright Electron, computer use, or an equivalent deterministic path for relevant Chromium surfaces.
6. Use computer use or an equivalent native harness for relevant menus, dialogs, tray items, permissions, window chrome, and drag and drop.
7. Preserve only the console, exception, network, target, DOM, accessibility, screenshot, process, persistence, and packaged-artifact evidence relevant to the selected proof.

## Shared completion rule

1. Environment readiness is not behavior verification.
2. Compilation and unit tests alone are not end-to-end proof when the claim concerns real runtime behavior.
3. A screenshot alone does not prove a claimed interaction or side effect; capture the action and observable outcome when those are the acceptance criteria.
4. Every verified review fix returns through the affected selected automated and runtime layers.
5. User-requested and repository-required checks remain completion gates. Failed or blocked required checks leave verification incomplete; optional omissions stay visible and cannot be relabeled as passing.
6. When a project-local harness exists, preserve its supported scenario identifiers and evidence with the platform results. Use mapped feature identifiers and structured receipts when the bundled format is selected; equivalent project formats remain valid.

## Tools and readiness

The bundled iOS, macOS, and Electron skills are first-class verification paths. Discover available tools and use an existing equivalent project command or harness when it already proves the required behavior. Specialized performance, device, signing, packaging, and protocol checks apply when their boundary affects the claim or the project requires them.

The Apple readiness doctor and Electron CDP doctor are optional diagnostics unless explicitly required by the user or project. A successful supported build, test, or harness preflight can establish the relevant readiness. An unavailable doctor, CDP connection, Playwright install, or Simulator does not block an unrelated check. Readiness never replaces behavioral proof.

## Agent use

1. The three focused platform skills are installed directly and are the invocation surfaces in Codex; the Apple route remains compatible with existing workflows.
2. `agents/apple-runtime-verifier.md` and `agents/electron-runtime-verifier.md` are portable specialist specifications, not separately registered Codex agent names.
3. When delegation is available and authorized, give a verification worker the relevant agent file and require it to read the referenced platform skill in full.
4. Without delegation, the primary agent follows the same specification directly.
