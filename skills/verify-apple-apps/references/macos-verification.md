# macOS verification

## Select the proof layers

1. Pure logic and models: focused Swift Testing or XCTest; broaden to the owning suite when integration risk or the project contract calls for it.
2. Windows, menus, commands, settings, drag and drop, pasteboard, files, and application lifecycle: focused tests where practical and direct runtime proof through computer use or an equivalent project harness for affected user paths.
3. Permissions, sandboxing, entitlements, login items, helpers, extensions, notifications, accessibility, audio, or screen capture: production-representative signing and bundle verification plus direct system evidence.
4. Rendering: snapshot only when rendering is the contract, then inspect the real window at relevant sizes, appearances, and accessibility settings.
5. Crashes, hangs, leaks, concurrency, or performance: reproduce first and route to logs, LLDB, Instruments, memgraph, traces, or dedicated platform skills.

## Build and test

1. Discover whether the repository uses an Xcode workspace, project, or Swift package and use its documented entrypoint.
2. Select focused tests, broader suites, static checks, and app builds according to the changed boundary and required checks. A library-owned logic change can use `swift test` without launching an app or setting up desktop control.
3. For app runtime proof, prefer a repository-owned build-and-run script when it exists. Otherwise build the actual application target. Available macOS build/run, SwiftPM, logging, and debugging tools are useful options; this skill supplies guidance, not those executables. An existing equivalent entrypoint does not need replacement or Run-button configuration just to verify a change.
4. Verify the current bundle path, identifier, version, signing identity, entitlements, architecture, and embedded helpers when the change touches packaging or system integration.
5. Rebuild and relaunch when the current runtime artifact could be stale. SwiftPM AppKit or SwiftUI GUI products need their project-supported `.app` bundle context; raw executable launch is suitable for command-line products.

## Drive the application

1. Confirm the launched process belongs to the artifact just built.
2. Use accessibility-backed computer use or the repository's equivalent native harness for windows, menus, controls, text, scrolling, and keyboard paths.
3. Read fresh application state after navigation or layout changes; do not reuse stale element indexes.
4. Use screenshots when accessibility state cannot prove layout, animation, focus, or visual output.
5. Exercise keyboard shortcuts, menu commands, multiple-window behavior, activation, relaunch, and persistence when they are in the blast radius.
6. For menu bar or background-only apps, verify both process state and the actual status-item or system interaction.

## Evidence and cleanup

1. Capture selected test results, build logs, artifact identity, process identity, before-and-after UI state, screenshots, unified logs, persisted values, files, and crash reports relevant to the change.
2. Use a temporary data directory or dedicated test profile when the app supports it.
3. Do not reset real user preferences, permissions, containers, keychain items, or files solely for convenience.
4. Stop only the process and log streams started by the run. Preserve the evidence bundle.
