---
name: verify-apple-apps
description: Verify iOS and macOS changes through focused and full tests, production-representative builds, Simulator or app interaction, logs, screenshots, and independent runtime evidence.
---

# Verify Apple Apps

Apply `$prove-the-work`. This skill specializes its verification ladder for Apple applications.

## Route the work

1. Read the repository instructions, schemes, test plans, targets, package graph, and existing verification scripts.
2. Classify the changed behavior: pure logic, feature state, rendering, navigation, persistence, networking, lifecycle, permissions, system integration, concurrency, or performance.
3. Read [references/ios-verification.md](references/ios-verification.md) for iOS, Simulator, XCUITest, Maestro, or device-readiness work.
4. Read [references/macos-verification.md](references/macos-verification.md) for macOS app, menu, window, permission, sandbox, or system-integration work.
5. Select the layers that can catch the actual failure and scale their depth to the change's risk. Name useful layers that are unavailable or intentionally omitted.

## Verification contract

1. Define the exact invariant, original failure path, nearby regression path, and observable completion evidence.
2. Prefer focused Swift Testing, XCTest, reducer, dependency, or model tests when the owning boundary can be exercised meaningfully. For a defect, demonstrate that the focused test fails for the original reason when practical.
3. Use snapshot tests only when rendered output is the contract, and visually inspect every changed reference before accepting it.
4. Run focused tests and select broader test plans, suites, and application builds according to integration, target, signing, entitlement, and release risk. Save `.xcresult` bundles when Xcode runs tests.
5. If runtime verification is selected, rebuild, install, and launch the current artifact. Do not verify a stale application already present on the Simulator or Mac.
6. When runtime behavior needs direct evidence, drive the real user path with the strongest available surface: existing XCUITest or Maestro flow, Xcode-aware Simulator tooling, computer use, or a deterministic project script.
7. During runtime verification, prefer accessibility identifiers and labels. Use coordinates only when semantic interaction is unavailable, and re-inspect state before reusing them.
8. Capture the before-and-after UI state, screenshots, logs, process health, persisted state, side effects, and crash evidence relevant to the selected proof.
9. Repeat timing-sensitive, lifecycle, crash, or concurrency paths when they are in scope. Use Xcode test repetition options when the failure is testable there.
10. Build for a generic device or the repository's distribution configuration when signing, entitlements, extensions, architecture, or device-only behavior is in scope.
11. Rerun affected layers after every verified review fix.

## Doctor

Run `python3 <skill-root>/scripts/apple_verification_doctor.py --platform ios` before Simulator verification or `--platform macos` before macOS verification. Add `--simulator-id`, `--bundle-id`, or `--process-name` when known. Treat the report as environment readiness only, never as behavior proof.

## Completion evidence

Return the commands, scheme and destination, focused and full test results, `.xcresult` paths, build configuration, artifact identity, interaction path, screenshots or state readback, logs and side effects, repetition count, blast-radius check, and every blocked layer. Do not call a Simulator-only pass physical-device verification.
