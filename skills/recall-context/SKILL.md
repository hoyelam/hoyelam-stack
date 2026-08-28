---
name: recall-context
description: Reconstruct the current state of prior work from in-scope task history, repository evidence, and live state before resuming or making a related change.
---

# Recall Context

## Scope

1. Restate the topic, repository, and time window being reconstructed. Default to the active project and the smallest recent window that can answer the request.
2. Read only in-scope tasks and records. Do not search unrelated projects or private conversations.
3. Skip history mining when the user already supplied a complete and current state capsule.

## Reconstruction

1. Find the most relevant prior tasks through the runtime's task-history tools or the user-provided record.
2. Extract decisions, rejected approaches, user corrections, unfinished work, verification results, paths, branches, commits, and external blockers.
3. Inspect the live repository and runtime state before trusting the old record. History describes what was true; the working tree shows what is true now.
4. Reconcile contradictions in favor of direct current evidence, and label unresolved conflicts.
5. Read shared engineering evidence when it materially changes the story: source history, issues, pull requests, architecture documents, build state, and runtime failures.

## State capsule

Return:

1. Current objective and status.
2. Confirmed decisions and constraints.
3. Relevant files, branch, commit, and worktree state.
4. Verification already completed and evidence still missing.
5. Open risks or blockers.
6. The smallest safe next action.

Keep the capsule compact enough to guide the next action without importing whole transcripts into the active context.
