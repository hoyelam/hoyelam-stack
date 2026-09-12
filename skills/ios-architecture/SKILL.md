---
name: ios-architecture
description: TCA and Point-Free architecture for Apple projects that use or explicitly adopt them.
---

# iOS Architecture

## Fit the project

1. Use neighboring features for an existing pattern, architecture docs for boundary decisions, and package manifests for dependency or adoption changes. Read tests when their contracts affect the change; no full architecture survey is required for a local edit.
2. Preserve an established architecture unless the request explicitly includes migration or the existing boundary cannot satisfy the requirement safely.
3. Prefer Composable Architecture for new stateful feature boundaries when the repository already uses it or has explicitly chosen it.

## Point-Free routing

Use only the installed skills relevant to the task:

1. `pfw-composable-architecture` for reducers, state, actions, effects, presentation, and feature composition.
2. `pfw-dependencies` for controllable side effects and test overrides.
3. `pfw-testing` for deterministic reducer and dependency tests.
4. `pfw-modern-swiftui`, `pfw-observable-models`, or `pfw-swift-navigation` when the existing feature uses those patterns.
5. `swift-concurrency` or `swift-concurrency-expert` for isolation, cancellation, sendability, and task-lifecycle concerns.

## Implementation rules

1. Keep state, actions, and view behavior consistent with the feature's existing model.
2. Put side effects behind dependencies that can be replaced in tests.
3. Keep views declarative and feature logic testable outside the UI.
4. Make invalid states difficult or impossible to represent.
5. Follow existing composition, navigation, persistence, and dependency conventions.
6. Prefer reducer or model unit tests for behavioral paths that can be exercised meaningfully.
7. Add snapshot tests only when rendering or layout is materially changed.
8. Build and run the real target in the Simulator or on macOS when runtime behavior, target integration, or user-visible output needs direct evidence.
