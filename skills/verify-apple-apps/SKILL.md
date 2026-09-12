---
name: verify-apple-apps
description: Route mixed Apple-platform verification or existing verify-apple-apps workflows.
---

# Verify Apple Apps

This explicit-only compatibility entrypoint routes to the focused platform skills. Existing `$verify-apple-apps` invocations remain supported; ordinary discovery uses the focused iOS and macOS skills.

## Route the work

1. For iOS, use [verify-ios-apps](../verify-ios-apps/SKILL.md).
2. For macOS, use [verify-macos-apps](../verify-macos-apps/SKILL.md).
3. For shared changes, select the affected platforms and combine their evidence without repeating unaffected checks.

Both entrypoints use the [shared Apple verification contract](references/verification-contract.md), platform references, and the existing optional readiness doctor. Load only the platform guidance needed for the task.
