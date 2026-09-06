---
name: orchestrate-project
description: Coordinate substantial programs across independent units or sessions through scoped delegation, durable progress, review, and verification of the integrated result. Collapse work one agent can finish directly.
---

# Orchestrate Project

Verification governs the program: a worker finishing creates a result to inspect, and acceptance requires evidence for the current artifact. The coordinator owns the outcome, dependency decisions, integration, and user report.

## Choose the scale and tools

1. Use this playbook for a standing program that outlives one task context or needs ongoing coordination of independently executable units. Ordinary features, fixes, and ambitious single-session tasks stay in `$hoyelam-mode`, with bounded delegation where useful.
2. Collapse to direct work when one agent can reasonably implement and verify the outcome. Retain verification inline without creating a program store or extra roles.
3. Use the project's existing coordination records when they can preserve the contract below. Otherwise use the [bundled runtime](references/bundled-runtime.md), which provides assignments, exclusive scope leases, inbox events, verification receipts, and recovery. Select one authoritative record; do not maintain competing boards.
4. Use available authorized delegation tools. In Codex, follow the [Codex adapter](../hoyelam-mode/references/codex-delegation.md); use the [Herdr adapter](../hoyelam-mode/references/herdr-delegation.md) when requested. No particular hosting service, model, PR stack tool, or CI service is required.
5. Coordination preserves the user's scope and authorization. A request to implement does not by itself authorize publishing, merging, deployment, destructive operations, or external messages.

## Roles and records

- **Coordinator:** frames the outcome, authors briefs, assigns exclusive scope, inspects results, maintains dependency context, and accepts verified integration. Delegate implementation while coordinating concurrent work; perform small integration work directly when it is safe and cheaper than another handoff.
- **Worker:** owns one bounded implementation or investigation and returns its actual changes and evidence. One writer owns each mutable boundary, including branches, worktrees, overlapping paths, simulators, and accounts.
- **Verifier or reviewer:** independently challenges expensive, judgment-heavy, or high-impact evidence and changes. A cheap deterministic check can be run by the worker and spot-checked by the coordinator. Review depth follows `$review-and-resolve`.
- Add a track coordinator only when the lead cannot manage the ready units directly; keep the tree shallow and its concurrency within runtime limits.

Persist the completion predicate, standing instructions, units and dependencies, briefs, exclusive resource ownership, worker/session identities and attempt numbers, results, current artifact identities, verification receipts, decisions, and unresolved gates. Existing files or runtime records are sufficient when they preserve these facts across interruption. Derive status from them. Store sensitive task evidence according to the project's conventions; keep local scratch records out of commits unless requested.

## Playbook

1. **Frame success and verification.** Define the program's observable completion predicate. Break it into independently writable and verifiable units, with acceptance criteria, exact checks, prerequisites, expected observations, and evidence per unit. Plan integration checks as well. Identify required checks and expose feasibility gaps before dependent implementation. Record standing instructions before the first assignment.
2. **Brief and pilot.** Use the [worker brief](references/worker-brief.md). Relay dependency outputs, not just unit names. Run one representative unit through implementation, verification, review, and local integration before broad fan-out. Correct the brief or verification recipe from its results. For cheap repeated units, the first ordinary unit is enough; no extra pilot roles are needed.
3. **Delegate ready work.** Assign only units whose dependency evidence is current and accepted. Record the worker, session, attempt, and exclusive scope before it writes. Use bounded rolling concurrency, refilling as units finish. When delegation is unavailable, execute sequentially and report that boundary. Every new or resumed assignment receives current standing instructions and consolidated context.
4. **Drain and assess results.** Queue completion reports while finishing a critical edit, brief, or state update. At a safe boundary, reconcile each report with its assignment and current attempt. Classify it as ready for verification, failed, blocked, cancelled, or stale; completion notifications alone do not establish success. Preserve evidence and release resource ownership before reassignment. Continue useful independent work around failures or human gates.
5. **Verify, review, and resolve.** Inspect actual diffs and receipts using `$prove-the-work` and `$review-and-resolve`. Validate findings, automatically fix confirmed issues within authorized scope, and rerun affected checks on the revised state. Failed behavior gets a scoped fix; blocked verification stays incomplete. Preserve failed attempts. A reviewer assertion, passing CI, or environment readiness alone cannot prove acceptance.
6. **Integrate continuously.** Integrate accepted units locally as dependencies permit, then run the selected integration checks before dependent work proceeds. Keep one owner of each integration branch. Identify the exact combined artifact, including uncommitted changes; passing each unit alone does not prove their composition. If PRs or stacks are part of the authorized work, track their current heads and dependency order and re-verify affected behavior after restacks or conflict fixes. Publishing and landing require their own authority.
7. **Close against evidence.** Reconcile every assignment to an outcome and release all active ownership. Check the original program predicate on the integrated final artifact, all required acceptance and review evidence, and any unresolved gates. Report completed units, failed or blocked checks, abandoned scope, evidence locations, and the next action for any blocker. Abandoning a required unit does not satisfy the original predicate; scope can change only within user authorization. Close bookkeeping separately from claiming successful completion.

## Verification receipts

Bind every verdict to the exact unit revision or artifact and the relevant fixtures, configuration, and harness version. Record the command or interaction, expected and observed outcome, test counts and exit status where applicable, artifact paths, and `passed`, `failed`, `blocked`, or `not run`. A revision change makes the old receipt insufficient for the new artifact; rerun affected checks and explicitly justify any carried-forward evidence for unaffected claims.

For runtime proof, identify the application instance, the exercised user path, readiness observations, and resulting state or side effects. Use the project's existing evidence format or the bundled harness fields when that format is selected. A doctor checks readiness, not the feature. Route platform work through `$verify-ios-apps`, `$verify-macos-apps`, or `$verify-electron-apps`.

## Recovery and bounded retries

On resume, read durable records before spawning. Reconcile actual worktrees, running workers, attempts, exclusive scopes, latest reports, and current artifacts. A late result must match the current assignment and dependencies before it is accepted; preserve useful findings from stale work without blindly integrating it.

Retry only after diagnosing the failure, with a finite budget appropriate to its cause. Narrow scope for capacity failures, repair broken prerequisites, and stop repeated unchanged infrastructure retries with a precise handoff. Preserve completed work and route around blocked units. Missing or corrupt records must be reconciled or restored before more assignments can safely write.

For design provenance and adaptations, see [design evidence](../../docs/design-evidence.md).
