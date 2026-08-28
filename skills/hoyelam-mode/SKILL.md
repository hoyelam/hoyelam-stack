---
name: hoyelam-mode
description: Select and run a proportionate root-cause-first workflow for non-trivial engineering tasks by inspecting available repository guidance, tests, builds, skills, and runtime tooling.
---

# Hoyelam Mode

Apply `$i-have-adhd` throughout the task.

## Choose the workflow

1. Inspect the request, task risk, repository instructions, architecture, owning surface, existing tests, supported builds, runtime harnesses, available skills, and environment capabilities.
2. Treat the workflow below as a preferred route and capability menu, not a mandatory sequence.
3. Select only layers that can materially improve the implementation or evidence. Combine, reorder, narrow, or omit layers when justified by the task.
4. Use more depth for changes involving security, privacy, destructive state, money, permissions, signing, concurrency, migrations, releases, or hard-to-reproduce failures.
5. State material unavailable, irrelevant, or disproportionate layers as boundaries. Never present an omitted layer as passing.
6. Include layers explicitly requested by the user unless they are genuinely blocked.
7. Keep selection lightweight. Do not narrate a workflow checklist when the choice is obvious.

## Scope gate

1. Preserve the requested scope. Investigation and review requests stay read-only unless the user also asks for changes.
2. For implementation work, continue through the selected verification and review layers without stopping after a plausible edit.
3. Ask only when a missing decision materially changes the result or requires new authority.
4. When resuming related work, run `$recall-context` before acting. When the user pauses unfinished work, run `$checkpoint-work` instead of forcing the normal completion rule.

## Preferred route

1. Read applicable `AGENTS.md`, repository documentation, and local instructions.
2. Use `$investigate-first` when the cause, ownership, regression history, or change boundary is not already established.
3. State the evidence-backed problem and smallest meaningful boundary before editing.
4. Read relevant architecture documentation and platform skills when they can affect the design. For iOS or macOS work, apply `$ios-architecture` when the repository uses or is adopting Composable Architecture or Point-Free libraries.
5. Implement the smallest complete root-cause solution that matches the existing architecture. Avoid compatibility layers, speculative abstractions, and unrelated cleanup.
6. Prefer focused unit tests for behavioral code when the owning boundary can be exercised meaningfully. Use snapshot tests only when visual or rendered structure is the behavior.
7. Select focused tests, broader suites, static checks, builds, and packaging based on the failure modes and risk of the change.
8. Use `$prove-the-work` when runtime behavior, integration, or user-visible outcomes need direct evidence. Use `$verify-apple-apps` for applicable iOS and macOS work, `$verify-electron-apps` for applicable Electron work, and `$build-verification-harness` when repeated real-app verification lacks a reliable control path.
9. Use `$comment-discipline` for code changes that add, retain, or touch comments, suppressions, directives, or workaround prose.
10. Use `$review-and-resolve` at a depth proportionate to the diff, risk, and architecture surface.
11. Resolve every verified in-scope finding and rerun the selected verification layers affected by the fix.
12. Report the root cause, implementation, selected evidence, review findings resolved, omitted or blocked layers, remaining boundaries, and worktree state.
13. After a complex or unusually costly task, use `$reflect-workflow` to propose durable improvements only when its evidence gate is satisfied.

## Completion rule

Completion requires evidence proportionate to the change and honest reporting of remaining boundaries; it does not require every workflow layer. Do not claim more than the selected evidence proves, and do not claim completion while verified in-scope findings remain unresolved.
