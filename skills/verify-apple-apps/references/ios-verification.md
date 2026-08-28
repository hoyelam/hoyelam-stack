# iOS verification

## Select the proof layers

1. Pure logic and models: Swift Testing or XCTest unit tests plus the full owning suite.
2. Composable Architecture features: reducer and dependency tests, effect cancellation and lifecycle coverage, then the real feature path.
3. SwiftUI or UIKit rendering: focused behavior tests, snapshots only when rendering is the contract, visual inspection, Dynamic Type and relevant appearance checks.
4. Navigation and interaction: existing XCUITest first when it is stable and owned by the repository; Maestro for black-box Simulator flows when already installed or when a reusable flow is explicitly being added.
5. Permissions, background work, notifications, extensions, deep links, audio, location, camera, and system surfaces: direct Simulator or device-path evidence plus logs and persisted side effects.
6. Concurrency, crashes, hangs, or timing: reproduce first, capture logs or traces, repeat the focused path, and use dedicated concurrency or performance skills when available.

## Build and test

1. Discover workspaces, projects, schemes, test plans, and available destinations rather than guessing them.
2. Use `xcodebuild test` with the repository's workspace or project, scheme, test plan when present, and an explicit Simulator destination.
3. Use `-only-testing` for the focused pass and the full test plan or scheme for regression coverage.
4. Write test results to a fresh `.xcresult` path outside tracked source. Preserve a failing result bundle when it contains diagnostic evidence.
5. For flaky or timing-sensitive XCTest paths, use `-test-repetitions`, `-run-tests-until-failure`, or the test plan's repetition settings with a stated stopping condition.
6. Build the application for the exact Simulator destination before runtime verification. For distribution-sensitive work, also build the generic iOS device destination or the repository's archive configuration.

Apple documents focused and repeated `xcodebuild` testing and `.xcresult` output in [Running tests and interpreting results](https://developer.apple.com/documentation/xcode/running-tests-and-interpreting-results). XCTest covers unit, performance, and UI testing in [XCTest](https://developer.apple.com/documentation/xctest).

## Drive the Simulator

1. Use an already booted, explicitly identified Simulator unless the task authorizes creating or booting another one.
2. Confirm the freshly built bundle identifier and installed artifact before launching.
3. Start scoped log capture before reproducing the path when diagnostics matter.
4. Inspect the accessibility tree or fresh screen state before each interaction sequence.
5. Prefer identifiers and labels for taps, typing, scrolling, and assertions. Re-read state after navigation or layout changes.
6. Capture the action and outcome, not only a final screenshot.
7. Use computer use when a real visual or system interaction is required and no narrower Simulator control surface exposes it.
8. If Simulator mirroring is available, confirm that real frames are updating before treating the mirror as proof.

## Maestro

1. Prefer repository-owned Maestro flows and configuration.
2. Use Maestro for repeatable black-box journeys through the iOS accessibility layer, especially multi-step UI regressions that do not need internal app instrumentation.
3. Keep flows deterministic: reset or seed state explicitly, use stable visible labels or identifiers, assert intermediate states, and isolate external services.
4. Run against the same current Simulator `.app` bundle being verified.
5. Preserve Maestro output and screenshots with the task evidence.
6. Do not install Maestro or introduce a new flow framework merely to avoid an existing reliable XCUITest or project harness without an explicit implementation need.

Maestro's iOS support drives Simulator apps through the accessibility layer as described in [Maestro iOS support](https://docs.maestro.dev/get-started/supported-platform/ios).

## State and cleanup

1. Use a dedicated test account, fixture, container, or Simulator state when available.
2. Reset permissions, app data, keychain assumptions, locale, appearance, or content size only when required for the scenario, and record the reset.
3. Terminate only the bundle being verified and stop only logs or helpers started by the run.
4. Preserve screenshots, `.xcresult` bundles, crash reports, logs, and generated outputs after cleanup.
