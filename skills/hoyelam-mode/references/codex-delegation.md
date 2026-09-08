# Codex delegation

Use Codex's available subagent tools and configured capacity. Do not hardcode a model name, context-window size, or child-count ceiling into the portable stack. Actual tool schemas and session instructions govern capabilities.

## Context

Send a self-contained brief with the goal, discovered context, owning paths, writable boundaries, and required evidence. Prefer `fork_turns: "none"` for that brief, or the smallest supported recent-history fork that carries needed decisions. Use full history only when relevant context cannot be conveyed reliably in a compact brief. Honor the runtime's rules for model inheritance and overrides.

Keep large logs and artifacts in task-owned files. Return the conclusion, useful excerpts, and paths the lead can inspect. Load only the skills and references that inform the assignment. A smaller prompt is useful only if it retains the context needed for correct work.

## Control

Reuse an idle worker when its role and context still fit. Send corrections to running workers; interrupt work that is wrong, unsafe, or no longer useful. Prefer completion notifications or bounded waits over polling, while keeping the lead's useful work moving.

Give concurrent writers exclusive files, worktrees, or mutable resources. Inspect returned changes and evidence before accepting them, and verify integration. Tool completion and worker confidence do not establish correctness.
