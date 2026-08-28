# Electron verification

## Process map

1. Main process: application lifecycle, windows, menus, tray, protocols, updates, native integrations, IPC registration, and privileged operations.
2. Preload: the security and type boundary between renderer code and exposed capabilities.
3. Renderer: DOM, UI state, routing, web APIs, network behavior, and user interaction.
4. Utility processes and workers: background computation, streaming, media, and crash isolation.
5. Native operating-system surfaces: file pickers, notifications, permissions, global shortcuts, window chrome, drag and drop, and accessibility behavior.

Every proof names which process owns the behavior and which other boundary can invalidate it.

## Automated layers

1. Unit-test pure functions, stores, reducers, serializers, and boundary validation.
2. Integration-test IPC channels, preload APIs, persistence, migrations, protocol handlers, and process lifecycle with explicit cleanup.
3. Use the repository's Playwright Electron or equivalent harness for renderer and cross-process flows when it already exists.
4. Test native modules and packaged-path behavior against the packaged artifact when development mode changes module loading or filesystem layout.
5. Run the complete relevant suite, type checking, linting, and packaging before the final runtime pass.

## Launch for inspection

1. Use the repository's supported launch command and a temporary user-data directory or project-defined test profile.
2. Bind remote debugging to loopback. Use an ephemeral or verified free port when the harness supports it.
3. Start renderer inspection with Electron's `--remote-debugging-port=<port>` switch.
4. Start main-process inspection with `--inspect=<port>` or `--inspect-brk=<port>` only when main-process debugging is required.
5. Record the launched process identifiers, artifact path, profile path, ports, and readiness signal.
6. Query `/json/version` and `/json/list`, then confirm target title, URL, type, and WebSocket endpoint before driving it.

Electron documents renderer DevTools in [Application debugging](https://www.electronjs.org/docs/latest/tutorial/application-debugging), main-process inspection in [Debugging the main process](https://www.electronjs.org/docs/latest/tutorial/debugging-main-process), and remote-debugging switches in [Supported command line switches](https://www.electronjs.org/docs/latest/api/command-line-switches).

## DevTools evidence

1. Runtime: capture uncaught exceptions, rejected promises, console errors, and evaluated state used to prove the invariant.
2. DOM and accessibility: assert stable roles, labels, attributes, visible text, focus, and state. Avoid coordinates for renderer content.
3. Network: record relevant request URL, method, status, response or failure, timing, cache or service-worker involvement, and WebSocket or event-stream messages.
4. Page and targets: detect reloads, renderer crashes, unexpected new windows, navigation, and target replacement.
5. Performance: capture a trace, CPU profile, heap evidence, or frame timing only when performance is in scope.
6. Storage and side effects: inspect only the isolated test profile or application-owned test data, never the user's normal browser or application profile.

The [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) provides Runtime, DOM, Accessibility, Network, Page, Target, Performance, Tracing, and storage domains. Prefer the protocol version exposed by the running Electron target because tip-of-tree protocol definitions can change.

## Real desktop interaction

1. Use DevTools or repository Playwright for Chromium content.
2. Use computer use for native menus, system dialogs, tray items, title bars, window management, file drag and drop, permissions, and other surfaces outside the DOM.
3. Inspect fresh application state after each native interaction and capture screenshots where accessibility state is insufficient.
4. Verify main-process or filesystem side effects independently after visible success.
5. Include reload, relaunch, multiple windows, offline or failed-network behavior, and close or quit lifecycle when they are in the blast radius.

## Cleanup

1. Close only targets and processes started by the verification run.
2. Stop protocol sessions and log capture before deleting scratch profiles.
3. Remove only the explicitly created temporary profile after evidence has been preserved.
4. Confirm no child, helper, debugging port, or temporary server from the run remains.
