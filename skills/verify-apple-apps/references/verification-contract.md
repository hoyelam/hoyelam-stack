# Shared Apple verification contract

Apply [prove-the-work](../../prove-the-work/SKILL.md). Inspect repository instructions, schemes or package products, test plans, and supported verification commands before choosing checks. Use the bundled platform guidance with available tools or an existing equivalent project workflow that proves the required behavior.

1. Define the invariant, original failure path where applicable, and observable acceptance evidence. Select checks according to the changed boundary and risk; user-requested and repository-required checks remain gates.
2. Prefer focused Swift Testing, XCTest, reducer, dependency, or model tests when that boundary can be exercised meaningfully. For a defect, demonstrate the original failure when practical.
3. Use snapshots when rendered output is the contract, and visually inspect changed references before accepting them.
4. Select broader test plans, suites, and application builds according to integration, target, signing, entitlement, and release risk. Save `.xcresult` bundles when Xcode runs tests. Pure logic or documentation changes do not automatically require app launch, a full suite, or distribution builds.
5. When runtime proof is needed, build and launch the current artifact through a suitable project command, Xcode-aware tool, Simulator control, or desktop harness. Confirm its identity so a stale installed app cannot stand in for the changed state.
6. Drive the relevant user path using an existing XCUITest or Maestro flow, Simulator tooling, computer use, or an equivalent deterministic project script. Prefer semantic interaction and refresh state after navigation or layout changes.
7. Capture the UI state, screenshots, logs, process health, persistence, side effects, or crash evidence that supports the selected claim. Repeat timing-sensitive paths with a stated stopping condition when they are in scope.
8. Use a device destination or distribution configuration when the claim depends on signing, entitlements, extensions, architecture, or device-only behavior. A generic device build does not prove execution on a physical device.
9. After review fixes, rerun affected checks on the final changed artifact. Retain unaffected evidence only when it is still current.

## Optional readiness diagnostic

When environment readiness is uncertain, use `python3 <verify-apple-apps-root>/scripts/apple_verification_doctor.py --platform ios` or `--platform macos`. Add `--simulator-id`, `--bundle-id`, or `--process-name` when useful. Resolve this shared script from [apple_verification_doctor.py](../scripts/apple_verification_doctor.py), including when entering through the focused skills.

The doctor is optional unless the project or user requires it. A supported build, test, or harness preflight may already establish readiness. Missing tooling unrelated to the selected proof does not block other checks; a doctor report never substitutes for behavior evidence.

## Completion evidence

Report the commands and selected test results with counts, tested state or artifact, scheme and destination when applicable, and relevant result bundles or runtime observations. Include blocked required checks and material unverified boundaries. Required checks that fail or are blocked leave verification incomplete; optional omissions are not passes. Do not demand an artifact, screenshot, repetition count, or device evidence for a claim that does not need it.
