---
name: hoyelam-mode
description: "Engineering task defaults for scope, autonomy, and verified completion."
---

# Hoyelam Mode

## Working preferences

Understand the intended outcome and relevant context. Choose the approach, tools, and depth that fit the task; there is no required sequence of phases or skill invocations. Make the smallest complete change that fits the project. Decide what would demonstrate success before dependent implementation; a short statement is enough for ordinary work.

For implementation requests, continue through the requested working result, relevant verification, and fixes to supported in-scope findings. Resolve routine choices independently. Ask when a missing decision materially changes the outcome or an action needs authority the task does not provide. Investigation and review remain read-only unless changes are authorized. Increase scrutiny for hard-to-reverse changes and realistic security, data, concurrency, or release risks.

## Orchestration

Use your judgment to work directly or delegate based on expected benefit to speed, quality, and context management. Task size alone does not require delegation. Choose useful assignments and concurrency as the work develops. When delegating, provide sufficient context, prevent conflicting writes, inspect returned results, and own decisions and final integration.

Honor user preferences and actual runtime limits. Use [delegation guidance](references/single-task-delegation.md) when it helps shape assignments or choose an execution route. Use `$orchestrate-project` and coordination records when dependencies, concurrent ownership, or continuity justify their overhead.

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
