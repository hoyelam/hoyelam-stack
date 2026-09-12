---
name: orchestrate-project
description: Coordinate work with dependencies, concurrent owners, or recovery across sessions.
---

# Orchestrate Project

Use this skill when dependencies, concurrent ownership, or continuity justify coordination. The lead owns decisions and the integrated outcome; choose direct or delegated work as needs change.

## Choose tools and records

Use [delegation guidance](../hoyelam-mode/references/single-task-delegation.md) for assignments, ownership boundaries, and execution routes. Keep one lead accountable; add coordination layers only when they solve a management bottleneck.

Use one record in existing project tools or a task-owned file. Preserve the goal, units, dependencies, owners, relevant instructions, results, artifacts, acceptance evidence, and open decisions. Add session identities, assignment attempts, and durable ownership when retries, concurrent writers, or interruptions require them. Keep scratch records out of commits unless requested.

The [bundled runtime](references/bundled-runtime.md) is optional. Select it when assignment identity, scope leases, inbox handling, or recovery helps; read its command contract then. No particular model or external service is required.

## Coordinate execution

1. **Assign.** Define observable success, writable units, and required unit and integration checks. Give workers authority, acceptance criteria, and current dependency outputs; the [compact brief](references/worker-brief.md) provides examples. Keep one writer per mutable resource, including branches, simulators, and accounts.
2. **Execute.** Start work when prerequisite evidence is current. Choose direct work, a pilot, or parallel assignments by expected benefit and reassess as results arrive. If a needed route is unavailable, continue useful direct work and report the effect on required outcomes.
3. **Assess.** Match reports to assignments and inspect changes and evidence. Distinguish success, failure, blockers, cancellation, and stale attempts. Use independent review when helpful. Fix confirmed in-scope issues, preserve failure evidence, and rerun affected checks; `$prove-the-work` and `$review-and-resolve` can help.
4. **Integrate.** Keep one integration owner. Identify the combined artifact, including uncommitted changes, and run integration checks. Rerun affected checks after restacks, conflict fixes, or later edits. Publishing, landing, deployment, and external messages need their own authority.

## Evidence and recovery

Tie evidence to the tested artifact, configuration, and fixtures. Record checks, expected and observed results, counts and exit status where applicable, and artifact paths. For runtime claims, identify the app instance, user path, and resulting state. Retain unaffected evidence while its claims remain current.

Before resuming writes, reconcile records with live workers, worktrees, ownership, attempts, dependencies, and artifacts; repair corrupt records first. Accept late results only when their assignment and dependencies still match. Release ownership before reassignment and preserve useful stale findings. Diagnose failures before retrying with a finite budget, and continue independent work around blockers.

Complete only when the original outcome is achieved, required checks pass on the integrated final state, in-scope findings are resolved, and assignments and ownership are accounted for. Worker reports and closed records alone do not prove completion. Report required failed or blocked checks and the next action.
