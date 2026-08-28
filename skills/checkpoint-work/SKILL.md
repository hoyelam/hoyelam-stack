---
name: checkpoint-work
description: Pause unfinished engineering work safely, preserving recoverable code and a precise state capsule without presenting the work as complete.
---

# Checkpoint Work

## Preserve

1. Confirm the repository, branch, scoped changes, and reason for pausing.
2. Finish the current atomic step or return it to a recoverable state. Start no new work solely to make the checkpoint look complete.
3. Inspect the diff and separate user-owned or unrelated changes from the work being checkpointed.
4. Run the cheapest meaningful checks that expose broken syntax, build state, or corrupted intermediate work. Record failures honestly; a checkpoint need not be green.
5. Preserve recoverable work through the repository's normal version-control workflow when the user authorized a checkpoint. Never discard changes to create a cleaner handoff.
6. Create or update a draft pull request only when explicitly requested or already part of the active workflow. Never imply review readiness.
7. Do not push, publish, or message external systems without authorization.

## State capsule

Record:

1. Objective and completed portions.
2. Exact remaining work in dependency order.
3. Current branch, commit, worktree state, and any remote state.
4. Tests, builds, and manual checks run, including failures.
5. Decisions made, rejected approaches, and architecture constraints.
6. Known defects, temporary scaffolding, permissions, and external blockers.
7. The first command or file to inspect when resuming.

## Resume rule

Use `$recall-context` before continuing. Reconcile the capsule with live repository state, then resume at the first unverified step rather than repeating completed work or assuming the checkpoint is current.
