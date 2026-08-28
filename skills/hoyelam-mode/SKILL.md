---
name: hoyelam-mode
description: Run the user's complete root-cause-first engineering workflow for non-trivial investigations, bug fixes, features, refactors, and implementation requests.
---

# Hoyelam Mode

Apply `$i-have-adhd` throughout the task.

## Scope gate

1. Preserve the requested scope. Investigation and review requests stay read-only unless the user also asks for changes.
2. For implementation work, continue through verification and review without stopping after a plausible edit.
3. Ask only when a missing decision materially changes the result or requires new authority.
4. When resuming related work, run `$recall-context` before acting. When the user pauses unfinished work, run `$checkpoint-work` instead of forcing the normal completion rule.

## Workflow

1. Read applicable `AGENTS.md`, repository documentation, and local instructions.
2. Run `$investigate-first` to establish the expected behavior, symptom, origin, actual repository, source location, callers, tests, history, and likely blast radius.
3. State the evidence-backed problem and smallest meaningful boundary before editing.
4. Read relevant architecture documentation and platform skills. For iOS or macOS work, apply `$ios-architecture` when the repository uses or is adopting Composable Architecture or Point-Free libraries.
5. Implement the smallest complete root-cause solution that matches the existing architecture. Avoid compatibility layers, speculative abstractions, and unrelated cleanup.
6. Make the behavior testable. Unit tests are mandatory for behavioral changes. Use snapshot tests only when visual or rendered structure is the behavior.
7. Run focused tests first, then the full relevant suite, static checks, and a production-representative build.
8. Run `$prove-the-work` against the real artifact with computer use or a deterministic script. Use `$verify-apple-apps` for iOS and macOS, `$verify-electron-apps` for Electron, and `$build-verification-harness` when the repository lacks a repeatable control path. Reproduce the original path and inspect runtime evidence.
9. Run `$comment-discipline` on the scoped diff.
10. Run `$review-and-resolve` across correctness, simplicity, architecture, concurrency, error handling, tests, and user experience.
11. Resolve every verified in-scope finding and rerun the affected tests, build, runtime check, comment audit, and diff review.
12. Report the root cause, implementation, tests, manual evidence, review findings resolved, remaining boundaries, and worktree state.
13. After a complex or unusually costly task, use `$reflect-workflow` to propose durable improvements only when its evidence gate is satisfied.

## Completion rule

Do not claim completion from compilation, unit tests alone, a reviewer self-report, or the presence of code. Completion requires passing automated checks, direct behavior evidence, a clean scoped review, and resolution of verified findings.
