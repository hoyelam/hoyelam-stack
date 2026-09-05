# hoyelam-stack working agreement

## Preferred engineering workflow

Treat this workflow as a decision aid, not a mandatory sequence. Verification is required for every change; its depth is proportionate to the work. First inspect the request, repository instructions, task risk, existing tests, supported build paths, runtime surfaces, and available tools and skills. Select, combine, reorder, or omit individual workflow layers according to what can materially prove the requested outcome.

Before implementation, first define observable acceptance criteria, then complete a distinct verification-planning step using [prove-the-work](skills/prove-the-work/SKILL.md). State how each criterion will be checked, with the exact command or interaction, prerequisites, expected result, and evidence to capture. Check feasibility and expose gaps before dependent implementation. Keep small plans in the task context and proceed within existing authorization. Establish or repair a project's supported verification path using the [project verification contract](skills/prove-the-work/references/project-verification.md).

For this repository, run `./scripts/validate.sh` from the repository root. It validates package structure and local documentation references, then runs the Python unittest suite. Success requires both validation and discovered tests to pass; inspect reported counts and skips. Workflow changes also need representative scenario review because structural checks cannot prove agent behavior.

1. Reconstruct relevant prior context when resuming older work, then reconcile it with live repository state.
2. Investigate enough to distinguish the request, expected behavior, origin, and smallest meaningful boundary before editing.
3. Locate the actual repository, applicable instructions, owning source, callers, tests, history, and adjacent behavior that matter to the change.
4. Read relevant architecture documentation and platform skills when they can change the implementation decision.
5. Fix the root cause with the smallest complete change that fits the existing architecture.
6. Prefer unit coverage for behavioral code. Use snapshot tests only when rendered output or visual structure is the behavior under test.
7. Choose focused checks, broader suites, static analysis, builds, and runtime interaction according to the failure modes they can catch.
8. Exercise the real behavior with computer use or a deterministic script when the change has a meaningful runtime surface and the environment supports it.
9. Use `verify-apple-apps` for relevant iOS and macOS verification and `verify-electron-apps` for relevant Electron verification.
10. After verification, review the complete scoped diff at a depth proportionate to its risk. Use independent review for substantial or risky changes when available and authorized; small low-risk changes can use self-review.
11. For authorized implementation, automatically resolve confirmed in-scope findings, then perform a distinct re-verification step on affected checks and the revised diff. Retain still-current evidence when review made no relevant changes.
12. When interrupted, preserve recoverable work and a precise resume capsule without claiming completion.
13. Use `orchestrate-project` only for independently executable work that spans units or sessions; collapse to direct work when one agent can reasonably finish it.

For larger changes, check each small verifiable unit before dependent work proceeds, then verify integration. When changing workflow behavior, follow [workflow validation](skills/hoyelam-mode/references/workflow-validation.md) using isolated tasks and observed results.

## Hard boundaries

1. Preserve the user's scope and authorization limits.
2. Treat a workflow or verification layer explicitly requested by the user as required unless it is genuinely blocked.
3. Follow closer repository instructions when they conflict with a general preference here.
4. Never report an omitted, unavailable, or blocked verification layer as passing.
5. Increase verification depth for security, privacy, data loss, money, permissions, signing, concurrency, migration, and release risk.
6. Resolve verified in-scope findings before claiming completion.
7. Do not perform destructive or external actions without the required authority.
8. Completion requires passing acceptance criteria and required checks on the final changed state. Failed or blocked required checks leave verification incomplete; finish independent work and report the blocker without claiming completion.
9. Preserve failure evidence. Do not weaken tests to get a pass or reuse stale results after affected implementation, fixture, configuration, or review changes.

## Comments

1. Prefer code, types, names, tests, runtime checks, and tooling over comments.
2. Keep legal and license headers.
3. Keep a comment only for a proven external constraint that cannot be made obvious or executable.
4. Prefix rare constraint comments with exactly one of `IMPORTANT`, `DO NOT REMOVE`, `TOO RISKY`, or `FINE FOR NOW`.
5. Every prefixed comment must name the external constraint, evidence source, failure mode, and removal condition when one exists.
6. Treat the prefix as a review trigger, not proof that the comment deserves to remain.
7. Remove narration, section banners, commented-out code, workaround stories, stale TODOs, and comments that repeat the code.
