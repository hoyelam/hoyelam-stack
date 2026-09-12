---
name: verify-macos-apps
description: Verify macOS behavior with relevant tests, app builds, and desktop or system evidence.
---

# Verify macOS Apps

Use the [shared Apple verification contract](../verify-apple-apps/references/verification-contract.md) and [macOS guidance](../verify-apple-apps/references/macos-verification.md). Choose checks for the changed logic, window, menu, lifecycle, persistence, permission, packaging, or system boundary; retain required checks as completion gates.

Use the repository's supported verification commands when they fit. This skill bundles macOS verification guidance and shares the Apple readiness helper; it does not install platform tools. Available options include Swift Testing, XCTest, `xcodebuild`, SwiftPM, app bundle launch, computer use, unified logs, and LLDB. Check availability and choose tools by the product and proof required; an equivalent existing harness needs no replacement, Simulator setup, or mandatory doctor run.

For GUI runtime claims, verify the current app bundle and relevant desktop behavior. A library-only Swift package may need only package checks. Inspect signing, entitlements, helpers, permissions, or distribution packaging when those boundaries affect the claim.
