---
name: checkpoint-work
description: Pause unfinished work with recoverable state and a compact handoff.
---

# Checkpoint Work

Finish the current atomic step or leave it recoverable. Inspect the scoped diff and distinguish unrelated or user-owned changes. Start no new work solely to make the checkpoint look complete, and never discard changes for a cleaner handoff.

Run the cheapest meaningful checks when they can expose broken intermediate work. Record failures honestly; a checkpoint need not be green and does not imply completion or review readiness.

Preserve work through the repository's normal version-control workflow within existing authorization. Create or update a draft pull request only when requested or already part of the active workflow. Pushing, publishing, and external messages still require authorization.

Leave a compact record that lets the next owner continue without rereading the task history. Use the shared [continuity record](../recall-context/references/continuity-record.md) when a handoff needs structure. On resumption, reconcile that record with live state and continue from the first unverified step. `$recall-context` is available when reconstruction needs more work.
