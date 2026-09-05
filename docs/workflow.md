# Preferred workflow

## Selection rule

1. Inspect the task type, changed surface, repository instructions, existing test and build commands, runtime harnesses, available tools, environment limits, and potential impact.
2. Choose the layers that can catch a realistic failure for this change.
3. Use the full root-cause, implementation, testing, runtime verification, and review path as the preferred default for substantial behavioral work.
4. Combine, reorder, narrow, or omit layers when they are irrelevant, redundant, unavailable, or disproportionate to the risk.
5. Name material omissions and residual uncertainty. An unavailable layer is a boundary, not a failure and not a pass.
6. Preserve hard safety, authorization, repository, and evidence-truthfulness requirements regardless of the selected workflow.
7. Include any workflow or verification layer the user explicitly requested unless it is genuinely blocked.
8. Route project-scale programs with independently executable units or multi-session coordination through `$orchestrate-project`; do not use it for work one agent can finish directly.
9. Within one direct task, keep metadata discovery and integration in the parent and delegate only independent evidence streams that earn their coordination cost.
10. When the user requests Herdr orchestration, use the [Herdr delegation adapter](../skills/hoyelam-mode/references/herdr-delegation.md). Hoyelam-mode retains workflow and completion decisions; Herdr supplies worker panes. Otherwise use native delegation when available and useful. Running inside Herdr alone does not activate orchestration.

## Available phases

1. `Recalling`: when work is resumed, reconcile relevant prior decisions with current repository state.
2. `Investigating`: establish expected behavior, symptom, origin, repository, evidence, and completion condition.
3. `Locating`: find owning source, callers, tests, history, architecture documents, and adjacent behavior.
4. `Isolating`: choose the smallest feature or defect boundary that can be changed and proved independently.
5. `Implementing`: fit the smallest complete root-cause solution into the existing architecture.
6. `Testing`: add useful automated coverage, then run the checks that address the change's plausible failure modes.
7. `Verifying`: when applicable, build the real artifact and exercise the exact behavior with computer use or a deterministic script.
8. `Reviewing`: audit the dimensions relevant to the diff, such as comments, correctness, simplicity, architecture, lifecycle, tests, and user experience.
9. `Resolving`: fix every verified in-scope finding and return to testing and verification.
10. `Orchestrating`: for project-scale work, persist units, dependencies, inbox events, gates, and revision-bound verification outside the conversation.
11. `Delegating`: for one direct task, route `0–3` bounded evidence streams while the parent retains decisions and synthesis.
12. `Complete`: report direct evidence, remaining boundaries, and worktree state.
13. `Checkpointed`: when interrupted, preserve recoverable work and a precise resume capsule without claiming completion.

## Investigation standard

1. The working directory is a hint, not proof of repository ownership.
2. A stack trace is a starting point, not automatically the root cause.
3. History matters when the symptom is a regression or a deliberate compromise.
4. Runtime evidence outranks a plausible source-only explanation.
5. The implementation boundary should be named before edits begin.

## Implementation standard

1. Preserve established architecture and conventions.
2. Read authoritative documentation for external APIs and unstable platform behavior.
3. Make state and side effects testable.
4. Prefer deletion, direct modeling, and small boundaries over wrappers and compatibility layers.
5. Keep unrelated cleanup out of the change.

## Verification standard

1. Unit tests are the preferred default for behavioral code when they can meaningfully exercise the owning boundary.
2. Snapshot tests are conditional on rendered output being the contract.
3. Focused tests provide fast diagnosis; broader suites are useful when the change has meaningful integration risk.
4. A production-representative build is valuable when target, entitlement, linkage, packaging, or configuration behavior can differ.
5. Direct runtime evidence is valuable when the changed behavior manifests in a real application surface.
6. Every review fix returns through the selected verification steps it can affect.
7. Repositories without a reliable real-app control path should gain a project-local verification harness and indexed feature map rather than inventing a new manual recipe for every task.
8. iOS and macOS verification follows `$verify-apple-apps`; Electron verification follows `$verify-electron-apps`.
9. When an existing harness or feature map may have drifted, use `$maintain-verification-harness` to reconcile source and drive the mapped behavior before relying on it.

## Completion report

Report only applicable evidence:

1. Root cause or satisfied requirement.
2. Owning boundary and implementation.
3. Automated coverage and checks selected.
4. Build and runtime evidence selected.
5. Verified review findings resolved.
6. Omitted or blocked layers and residual uncertainty.
7. Remaining external or out-of-scope work.
8. Branch, commit, and worktree state when relevant.
