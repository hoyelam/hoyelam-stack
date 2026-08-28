---
name: ios-architecture
description: Guide iOS and macOS implementation when a repository uses or is adopting Composable Architecture and Point-Free libraries, while preserving the project's existing architecture and test conventions.
---

# iOS Architecture

## Architecture gate

1. Read the repository's `AGENTS.md`, architecture docs, package manifest, neighboring features, and tests before selecting a pattern.
2. Preserve an established architecture unless the request explicitly includes migration or the existing boundary cannot satisfy the requirement safely.
3. Prefer Composable Architecture for new stateful feature boundaries when the repository already uses it or has explicitly chosen it.
4. Treat “BFW” as the Point-Free `pfw-*` skill family unless the repository defines another meaning.

## Point-Free routing

Use only the installed skills relevant to the task:

1. `pfw-composable-architecture` for reducers, state, actions, effects, presentation, and feature composition.
2. `pfw-dependencies` for controllable side effects and test overrides.
3. `pfw-testing` for deterministic reducer and dependency tests.
4. `pfw-modern-swiftui`, `pfw-observable-models`, or `pfw-swift-navigation` when the existing feature uses those patterns.
5. `swift-concurrency` or `swift-concurrency-expert` for isolation, cancellation, sendability, and task-lifecycle concerns.

## Implementation rules

1. Model state and actions before writing view behavior.
2. Put side effects behind dependencies that can be replaced in tests.
3. Keep views declarative and feature logic testable outside the UI.
4. Make invalid states difficult or impossible to represent.
5. Follow existing composition, navigation, persistence, and dependency conventions.
6. Prefer reducer or model unit tests for behavioral paths that can be exercised meaningfully.
7. Add snapshot tests only when rendering or layout is materially changed.
8. Build and run the real target in the Simulator or on macOS when runtime behavior, target integration, or user-visible output needs direct evidence.
