# Delegation

Use this reference when a task benefits from parallel work or independent judgment. Substantial independent work should actively use a lead and workers; small or tightly dependent work can stay direct.

## Shape the work

The lead establishes the outcome and enough repository context to assign useful work. Delegate bounded investigation, implementation, verification, or review, including independent units within one repository. Share relevant discoveries so workers do not repeat a broad survey. Keep decisions and integration with one lead.

Each brief needs a goal, relevant source/context, exclusive writable scope or read-only boundary, and expected evidence. Add dependencies or recovery records when needed; the [worker brief](../../orchestrate-project/references/worker-brief.md) provides examples. Workers return results, changed paths, checks actually run, and unresolved questions. The lead inspects accepted changes, reconciles contradictions, and verifies the combined outcome.

Choose the useful number of workers within the runtime's available capacity and configured limits. Keep independently ready work moving while the lead integrates results. Isolate concurrent writers by files, worktrees, or mutable resources. Do not create parallel workers that duplicate the same discovery or contend for the same application instance.

## Execution adapters

Honor the user's selected runtime and model preferences. Use native delegation when available. Codex-specific context, reuse, and control guidance is in the [Codex adapter](codex-delegation.md); consult it when those mechanics matter.

When running in a managed Herdr environment (`HERDR_ENV=1`), or when Herdr is requested, use the [Herdr adapter](herdr-delegation.md) to check the session and route workers. Its operating details stay in that adapter. If automatic detection fails, report the relevant failure briefly and use available native delegation. An explicit requirement for Herdr remains a reported blocker if unavailable. Continue independent direct work when no delegation route works.
