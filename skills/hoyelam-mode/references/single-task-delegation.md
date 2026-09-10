# Delegation

Choose direct work or delegation by expected benefit. Task size and available capacity do not require workers.

## Shape the work

Give each worker a goal, relevant findings and source paths, a writable or read-only boundary, and expected evidence. Investigation, implementation, verification, and review can all be delegated. Add dependencies or recovery records when useful; see the [worker brief](../../orchestrate-project/references/worker-brief.md).

Choose worker count and timing within runtime limits, and reassess as results arrive. Share discoveries and isolate concurrent writers by files, worktrees, or mutable resources to avoid duplicate investigation and conflicting use of the same application instance.

Workers return results, changed paths, checks actually run, and unresolved questions. The lead owns decisions, inspects returned changes, resolves contradictory reports, and verifies integration.

## Execution adapters

Honor the user's runtime and model preferences. Otherwise, use native delegation when available; the [Codex adapter](codex-delegation.md) covers context and worker control.

For requested Herdr delegation or a managed Herdr environment (`HERDR_ENV=1`), use the [Herdr adapter](herdr-delegation.md). If automatic detection fails, report the failure and use native delegation. If Herdr was explicitly required, report it blocked instead. Continue useful direct work when no route is available.
