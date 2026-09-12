---
name: recall-context
description: Resume prior work by reconciling incomplete or stale context with current state.
---

# Recall Context

Start with the supplied handoff or nearest relevant task record. Search only the active project and the smallest history window that resolves missing decisions, evidence, or unfinished work. Do not search unrelated projects or private conversations. Skip history mining when the user supplied a complete current record.

Check the relevant live repository and runtime state before trusting history. Reconcile contradictions in favor of direct current evidence and label unresolved conflicts. Read source history, project records, or external build state only when they materially affect the next decision.

Return the current outcome and the next useful action with enough decisions, changed-state details, and verification gaps to support it. Use the shared [continuity record](references/continuity-record.md) when a durable handoff needs structure. Link to deeper evidence instead of importing transcripts. Resume from the first unverified step and retain still-current evidence for completed work.
