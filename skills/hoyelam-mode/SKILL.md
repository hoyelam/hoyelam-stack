---
name: hoyelam-mode
description: "Personal agent defaults: focused changes, active orchestration, and verified outcomes."
---

# Hoyelam Mode

## Working preferences

Understand the intended outcome and relevant context. Choose the approach, tools, and depth that fit the task; there is no required sequence of phases or skill invocations. Make the smallest complete change that fits the project. Decide what would demonstrate success before dependent implementation; a short statement is enough for ordinary work.

Continue independently within the user's authorized scope. Ask when missing information materially changes the outcome or new authority is needed. Investigation and review remain read-only unless changes are authorized. Increase scrutiny for hard-to-reverse changes and realistic security, data, concurrency, or release risks.

## Orchestration

For substantial work, actively act as the lead: identify independent investigation, implementation, verification, and review units and delegate when that improves elapsed time or confidence. Keep ready work moving. Own decisions, clear writable boundaries, returned evidence, and final integration. Work directly on small or tightly dependent tasks where a handoff adds no value.

Choose concurrency from useful independent work and actual runtime capacity. Give workers focused context and evidence requirements; avoid repeated broad discovery and full-history forks without a reason. Read [delegation guidance](references/single-task-delegation.md) when choosing a route or shaping assignments. Use `$orchestrate-project` when dependencies, concurrent ownership, or continuity need more coordination.

## Evidence and completion

Use existing project checks and exercise the changed behavior through its relevant interface. Review the scoped result, resolve supported in-scope findings, and rerun checks affected by later changes. Keep still-current evidence. A build, readiness check, or worker's completion message proves only what it actually observed.

Completion requires the intended outcome and required checks to pass on the final changed state. Inspect actual outputs and test discovery. Failed or blocked required checks leave verification incomplete; finish independent work and report the blocker. Never weaken checks to manufacture a pass. Report the result, meaningful evidence, and material uncertainty concisely.

## Available capabilities

Load skills and references only when they add useful guidance to the current task.

| Need | Capability |
| --- | --- |
| Unclear cause or ownership | `$investigate-first` |
| Verification design or uncertain evidence | `$prove-the-work` |
| Deeper review or comment audit | `$review-and-resolve`, `$comment-discipline` |
| Missing or drifting app control path | `$build-verification-harness`, `$maintain-verification-harness` |
| Platform-specific proof | `$verify-ios-apps`, `$verify-macos-apps`, `$verify-electron-apps` |
| Project-selected Point-Free architecture | `$ios-architecture` |
| Pause or reconstruct prior work | `$checkpoint-work`, `$recall-context` |
| Repeated friction or reusable lessons | `$reflect-workflow` |

Changes to these behavioral rules use [isolated workflow exercises](references/workflow-validation.md).
