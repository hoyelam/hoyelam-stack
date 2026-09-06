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
5. Select broader suites, type checking, linting, and packaging according to the affected boundary and repository-required checks. A pure logic check does not automatically need packaging or runtime launch.

## Launch for runtime proof

1. Use the repository's supported launch command and a temporary user-data directory or project-defined test profile.
2. Record the launched process identifiers, artifact path, profile path, and readiness signal. Use a project harness or desktop control without debugging ports when it can prove the required behavior.
3. If renderer inspection through CDP is selected, use Electron's `--remote-debugging-port=<port>` switch. Bind remote debugging to loopback and use an ephemeral or verified free port when supported.
4. Use `--inspect=<port>` or `--inspect-brk=<port>` only when main-process debugging is needed, with the inspector bound to loopback as well.
5. When connecting protocol tools, record the ports and confirm target identity before driving them. Query `/json/version` and `/json/list` or use the harness's equivalent identity check. Confirm the title, URL, type, and WebSocket endpoint belong to the current app.

Electron documents renderer DevTools in [Application debugging](https://www.electronjs.org/docs/latest/tutorial/application-debugging), main-process inspection in [Debugging the main process](https://www.electronjs.org/docs/latest/tutorial/debugging-main-process), and remote-debugging switches in [Supported command line switches](https://www.electronjs.org/docs/latest/api/command-line-switches).

## DevTools evidence

Use this guidance when DevTools supplies the selected proof; it is not required for every renderer or Electron change.

1. Runtime: capture uncaught exceptions, rejected promises, console errors, and evaluated state used to prove the invariant.
2. DOM and accessibility: assert stable roles, labels, attributes, visible text, focus, and state. Prefer semantic controls; if only visual interaction is available, inspect fresh state before using coordinates.
3. Network: record relevant request URL, method, status, response or failure, timing, cache or service-worker involvement, and WebSocket or event-stream messages.
4. Page and targets: detect reloads, renderer crashes, unexpected new windows, navigation, and target replacement.
5. Performance: capture a trace, CPU profile, heap evidence, or frame timing only when performance is in scope.
6. Storage and side effects: inspect only the isolated test profile or application-owned test data, never the user's normal browser or application profile.

The [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) provides Runtime, DOM, Accessibility, Network, Page, Target, Performance, Tracing, and storage domains. Prefer the protocol version exposed by the running Electron target because tip-of-tree protocol definitions can change.

## Real desktop interaction

1. Use a repository harness, DevTools, Playwright, computer use, or another available path that proves the Chromium interaction. These are alternatives; choosing one does not require installing the others.
2. Use computer use or an equivalent native harness for menus, system dialogs, tray items, title bars, window management, file drag and drop, permissions, and other surfaces outside the DOM.
3. Inspect fresh application state after each native interaction and capture screenshots where accessibility state is insufficient.
4. Verify main-process or filesystem side effects independently after visible success.
5. Include reload, relaunch, multiple windows, offline or failed-network behavior, and close or quit lifecycle when they are in the blast radius.

## Cleanup

1. Close only targets and processes started by the verification run.
2. Stop protocol sessions and log capture before deleting scratch profiles.
3. Remove only the explicitly created temporary profile after evidence has been preserved.
4. Confirm no child, helper, debugging port, or temporary server from the run remains.
