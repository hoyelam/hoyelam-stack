---
name: verify-ios-apps
description: Verify iOS behavior with relevant tests, builds, and Simulator or device evidence.
---

# Verify iOS Apps

Use the [shared Apple verification contract](../verify-apple-apps/references/verification-contract.md) and [iOS guidance](../verify-apple-apps/references/ios-verification.md). Choose checks for the changed logic, rendering, navigation, persistence, lifecycle, permissions, or system integration; retain required checks as completion gates.

Use the repository's supported verification commands when they fit. This skill bundles iOS verification guidance and shares the Apple readiness helper; it does not install platform tools. Available options include Swift Testing, XCTest, `xcodebuild`, XcodeBuildMCP Simulator build/run and UI tools, XCUITest, Maestro, and computer use. Check availability and choose by coverage and readiness; an equivalent existing harness needs no replacement or mandatory doctor run.

For runtime claims, verify the current app and relevant user path, preserving only the observations needed to prove it. Use device or distribution evidence when that behavior depends on it, and distinguish Simulator evidence from physical-device verification.
