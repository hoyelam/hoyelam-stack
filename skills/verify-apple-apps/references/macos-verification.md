# macOS verification

## Select the proof layers

1. Pure logic and models: Swift Testing or XCTest plus the full owning suite.
2. Windows, menus, commands, settings, drag and drop, pasteboard, files, and application lifecycle: focused tests where practical plus computer use against the rebuilt app.
3. Permissions, sandboxing, entitlements, login items, helpers, extensions, notifications, accessibility, audio, or screen capture: production-representative signing and bundle verification plus direct system evidence.
4. Rendering: snapshot only when rendering is the contract, then inspect the real window at relevant sizes, appearances, and accessibility settings.
5. Crashes, hangs, leaks, concurrency, or performance: reproduce first and route to logs, LLDB, Instruments, memgraph, traces, or dedicated platform skills.

## Build and test

1. Discover whether the repository uses an Xcode workspace, project, or Swift package and use its documented entrypoint.
2. Run the focused test, full relevant suite, static checks, and the real macOS application build.
3. Prefer a repository-owned build-and-run script when it exists. Otherwise build the actual application target, not only a library package.
4. Verify the current bundle path, identifier, version, signing identity, entitlements, architecture, and embedded helpers when the change touches packaging or system integration.
5. Rebuild and relaunch before every final runtime pass.

## Drive the application

1. Confirm the launched process belongs to the artifact just built.
2. Use accessibility-backed computer use for windows, menus, controls, text, scrolling, and keyboard paths.
3. Read fresh application state after navigation or layout changes; do not reuse stale element indexes.
4. Use screenshots when accessibility state cannot prove layout, animation, focus, or visual output.
5. Exercise keyboard shortcuts, menu commands, multiple-window behavior, activation, relaunch, and persistence when they are in the blast radius.
6. For menu bar or background-only apps, verify both process state and the actual status-item or system interaction.

## Evidence and cleanup

1. Capture focused and full test results, build logs, artifact identity, process identity, before-and-after UI state, screenshots, unified logs, persisted values, files, and crash reports relevant to the change.
2. Use a temporary data directory or dedicated test profile when the app supports it.
3. Do not reset real user preferences, permissions, containers, keychain items, or files solely for convenience.
4. Stop only the process and log streams started by the run. Preserve the evidence bundle.
