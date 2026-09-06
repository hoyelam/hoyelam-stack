# Preferred workflow

## Working sequence

1. Understand the request, repository, and smallest meaningful change.
2. Define success: the observable acceptance criteria and realistic failure modes.
3. Plan verification: map each criterion to the exact check or interaction, prerequisites, expected result, and evidence to capture. Check feasibility and expose gaps before implementation.
4. Implement the simplest complete solution in small verifiable units, checking each before dependent work proceeds.
5. Verify the implementation against the plan, including final integration and the original reproduction for regressions.
6. Review and resolve: review the complete scoped diff, validate findings, and automatically fix confirmed in-scope issues. Use independent review for substantial or risky changes when available and authorized.
7. Re-verify affected checks after fixes and inspect the revised diff. Repeat review and resolution when verified issues remain; retain current evidence if no relevant changes occurred.
8. Report evidence from the final state and explicit remaining boundaries. Failed or blocked required checks leave verification incomplete.

Verification planning is a distinct step before implementation. Keep it proportionate: a small edit can use one sentence, and ordinary planning does not require a new approval. See [prove-the-work](../skills/prove-the-work/SKILL.md) for the planning and evidence contract.

Read-only reviews remain read-only. Independent reviewers report supported findings; the implementation owner verifies them and owns accepted fixes. Small low-risk changes can use self-review. See [review-and-resolve](../skills/review-and-resolve/SKILL.md) for review selection and the resolution loop.

## Orchestration governed by verification

For substantial programs, [orchestrate-project](../skills/orchestrate-project/SKILL.md) turns the working sequence into scoped assignments and durable progress. The lead defines unit acceptance and integration checks before delegation, pilots a representative unit, uses bounded rolling concurrency, reviews returned evidence, and integrates accepted work continuously. Each dependency advances on verified results. The final combined artifact must satisfy the original outcome; completed workers alone do not prove it.

Use existing project records when they preserve ownership, attempts, dependencies, and current evidence. The bundled runtime supplies those safeguards when needed. Direct tasks keep the same evidence standard with less coordination. Optional automation packs schedule selected work only when configured; they are not a prerequisite for this method.

## Selection rule

1. Inspect the task type, changed surface, repository instructions, existing test and build commands, runtime harnesses, available tools, environment limits, and potential impact.
2. Choose the layers that can catch a realistic failure for this change.
3. Use the full root-cause, implementation, testing, runtime verification, and review path as the preferred default for substantial behavioral work.
4. Verification is required for every change. Combine, reorder, narrow, or omit individual optional layers when they are irrelevant, redundant, unavailable, or disproportionate to the risk.
5. Name material omissions and residual uncertainty. An unavailable required check leaves verification incomplete; it cannot be silently downgraded or reported as a pass.
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
5. `Planning verification`: turn acceptance criteria into executable checks, expected observations, evidence capture, and explicit prerequisites before implementation.
6. `Implementing`: fit the smallest complete root-cause solution into the existing architecture.
7. `Testing`: add useful automated coverage, then run the checks that address the change's plausible failure modes.
8. `Verifying`: when applicable, build the real artifact and exercise the exact behavior with computer use or a deterministic script.
9. `Reviewing`: audit the dimensions relevant to the diff, such as comments, correctness, simplicity, architecture, lifecycle, tests, and user experience.
10. `Resolving`: fix every verified in-scope finding and return to testing and verification.
11. `Orchestrating`: for project-scale work, persist units, dependencies, inbox events, gates, and revision-bound verification outside the conversation.
12. `Delegating`: for one direct task, route `0–3` bounded evidence streams while the parent retains decisions and synthesis.
13. `Complete`: report direct evidence, remaining boundaries, and worktree state.
14. `Checkpointed`: when interrupted, preserve recoverable work and a precise resume capsule without claiming completion.

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

Define observable acceptance criteria, then plan verification before implementation through [prove-the-work](../skills/prove-the-work/SKILL.md). Apply its evidence and completion gates to every project type, including documentation and tooling. Use the [project verification contract](../skills/prove-the-work/references/project-verification.md) when establishing or repairing a project's supported commands and local/CI requirements.

1. Unit tests are the preferred default for behavioral code when they can meaningfully exercise the owning boundary.
2. Snapshot tests are conditional on rendered output being the contract.
3. Focused tests provide fast diagnosis; broader suites are useful when the change has meaningful integration risk.
4. A production-representative build is valuable when target, entitlement, linkage, packaging, or configuration behavior can differ.
5. Direct runtime evidence is valuable when the changed behavior manifests in a real application surface.
6. Every review fix returns through the selected verification steps it can affect.
7. Repositories without a reliable real-app control path should gain a repeatable verification path that fits their existing tools and documentation; the bundled harness and feature-map template is available when needed.
8. iOS verification follows `$verify-ios-apps` and macOS verification follows `$verify-macos-apps`; Electron verification follows `$verify-electron-apps`.
9. When an existing harness or feature map may have drifted, use `$maintain-verification-harness` to reconcile source and drive the mapped behavior before relying on it.

For changes to this workflow, follow [workflow validation](../skills/hoyelam-mode/references/workflow-validation.md) and inspect actual task outputs. Unit tests and hypothetical scenario answers alone do not establish that agents follow the method during implementation.

The [initial 2026-09-05 implementation exercise](evidence/workflow-2026-09-05.md) records three isolated tasks and independent replay. The subsequent [workflow alignment exercise](evidence/workflow-alignment-2026-09-05.md) covers reuse of existing project records and blocked completion with the revised orchestration guidance. Each records the limits of its evidence.

## Completion report

Report only applicable evidence, tied to the final changed state. Mark checks as passed, failed, blocked, or not run. Completion requires passing acceptance criteria and required checks; a blocked required check needs an explicit incomplete outcome and the next action that would unblock verification.

1. Root cause or satisfied requirement.
2. Owning boundary and implementation.
3. Automated coverage and checks selected.
4. Build and runtime evidence selected.
5. Verified review findings resolved.
6. Omitted or blocked layers and residual uncertainty.
7. Remaining external or out-of-scope work.
8. Branch, commit, and worktree state when relevant.
