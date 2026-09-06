---
name: hoyelam-mode
description: Select and run a proportionate root-cause-first workflow for non-trivial engineering tasks by inspecting available repository guidance, tests, builds, skills, and runtime tooling.
---

# Hoyelam Mode

## Choose the workflow

1. Inspect the request, task risk, repository instructions, architecture, owning surface, existing tests, supported builds, runtime harnesses, available skills, and environment capabilities.
2. Treat the workflow below as a preferred route and capability menu, not a mandatory sequence.
3. Verification is required for every change; select its depth, not whether to verify. Combine, reorder, narrow, or omit individual layers when justified by the task.
4. Use more depth for changes involving security, privacy, destructive state, money, permissions, signing, concurrency, migrations, releases, or hard-to-reproduce failures.
5. State material unavailable, irrelevant, or disproportionate layers as boundaries. Never present an omitted layer as passing.
6. Include layers explicitly requested by the user unless they are genuinely blocked.
7. Keep selection lightweight. Do not narrate a workflow checklist when the choice is obvious.

## Define success

Establish the observable acceptance criteria and realistic failure modes before choosing an implementation. State what must be true when the work is complete.

## Plan verification

1. Before implementation, map each acceptance criterion to the exact check or interaction, required environment or fixtures, expected result, and evidence to capture. Distinguish required checks from optional evidence. Read `$prove-the-work` when designing or executing a verification contract, when evidence is ambiguous, or when the task needs its detailed receipt and completion rules.
2. Discover the project's verification contract in repository instructions, contributor documentation, scripts, or CI. When establishing or repairing that contract, use the [project verification contract](../prove-the-work/references/project-verification.md).
3. Check that the planned tools and control paths are available. Run a focused baseline when practical; reproduce regressions when a deterministic path exists. Identify missing tests, harness work, and blockers before dependent implementation, and plan any authorized verification setup explicitly.
4. State the verification plan, then proceed within the user's authorization; this step does not require a new approval. A small change can use one sentence in the task context, while complex work can use the project's existing plan or handoff record.
5. Carry the plan through implementation, review, and final verification. Revise it when scope or evidence changes, and expose unresolved verification gaps without silently weakening acceptance criteria. Documentation, configuration, libraries, services, scripts, and applications all require evidence suited to their actual output.

## Orchestrate substantial work

1. Orchestration is a core part of the method for substantial programs. Use `$orchestrate-project` for work that needs ongoing coordination across independently executable units or sessions. The coordinator owns scoped briefs, dependency context, integration, and current verification evidence; worker completion is a result to inspect.
2. Plan unit verification before delegation, accept units only after their required checks and review, and verify the combined result before claiming completion. Use existing project coordination tools or the bundled runtime.
3. Do not use orchestration merely because a task is difficult or contains several steps. Collapse to this skill's direct workflow when one agent can reasonably complete and verify the outcome.

## Single-task delegation

1. Keep task framing, repository and instruction discovery, worktree state, architecture selection, decomposition, authorization boundaries, and final integration in the parent.
2. Delegate only a meaningful evidence stream: a bounded investigation, specialist review, test or log analysis, documentation check, or independent implementation unit whose result can change the parent decision or materially reduce elapsed time.
3. Do not delegate metadata discovery, one obvious command, clerical restatement, tightly sequential reasoning, or shared writes that cost more to coordinate than to perform directly.
4. Give each child one independent goal, the relevant discovered context, an exclusive scope, exact evidence requirements, and a compact report contract. The child should not repeat the parent's broad repository survey.
5. Use the smallest useful number of children. Run `scripts/delegation_router.py --help` when the `0–3` route is not obvious.
6. The parent owns synthesis, verifies material claims, resolves contradictions, reviews every accepted change, and reports one integrated result.
7. Select the execution route only after deciding delegation is useful and authorized. Honor explicit user preferences, including native delegation or no delegation. Otherwise, when `HERDR_ENV=1` and the Herdr CLI is available, read [references/herdr-delegation.md](references/herdr-delegation.md), check the managed session with its read-only bootstrap steps, and automatically use Herdr when reachable. An explicit Herdr request also uses that adapter; no repeated orchestration prompt is needed for automatic selection.
8. Outside Herdr, or when automatic detection finds its CLI or managed session unavailable, use native delegation when available and authorized; in Codex, read [references/codex-delegation.md](references/codex-delegation.md) first. Briefly report a failed automatic Herdr check and the selected fallback. If the user explicitly requires Herdr, report the blocker instead of silently switching routes. When no route is available, continue useful direct work. Keep one parent responsible for assignments and integration across either route.

## Scope gate

1. Preserve the requested scope. Investigation and review requests stay read-only unless the user also asks for changes.
2. For implementation work, continue through the selected verification and review layers without stopping after a plausible edit.
3. Ask only when a missing decision materially changes the result or requires new authority.
4. When resuming related work, run `$recall-context` before acting. When the user pauses unfinished work, run `$checkpoint-work` instead of forcing the normal completion rule.

## Working sequence

1. **Understand.** Read repository instructions, owning source, callers, and relevant architecture guidance. Use `$investigate-first` when cause or ownership is unclear. State the evidence-backed problem and smallest meaningful boundary. Apply `$ios-architecture` when Point-Free architecture can affect an Apple-platform design.
2. **Define success.** Establish observable acceptance criteria and realistic failure modes as described above.
3. **Plan verification.** Map those criteria to feasible checks, prerequisites, expected results, and evidence before implementation.
4. **Implement.** Make the smallest complete root-cause change that fits the architecture. For larger work, choose small verifiable units and check each before dependent work builds on it; retain final integration checks. Unit boundaries do not require separate commits or delegation.
5. **Verify.** Execute the planned checks and capture current acceptance evidence; use `$prove-the-work` for detailed verification and receipt guidance. Use `$verify-ios-apps` for iOS, `$verify-macos-apps` for macOS and `$verify-electron-apps` for Electron. Use `$build-verification-harness` for a missing recurring real-app control path and `$maintain-verification-harness` for drift. For regressions, exercise the original reproduction through the same relevant interface after the fix; report when that proof is unavailable.
6. **Review and resolve.** Review the complete scoped diff through `$review-and-resolve`, including `$comment-discipline` for touched comments or directives. Use independent review for substantial or risky changes when available and authorized. Validate findings before automatically fixing confirmed in-scope issues; report out-of-scope work separately.
7. **Re-verify.** Rerun checks affected by review fixes on the final changed state and inspect the revised diff. Return to review and resolution when new verified issues remain. If review made no changes, retain still-current evidence; a distinct step does not require a redundant run.
8. **Report evidence.** Report the result, tested state, observed outcomes, resolved findings, and concrete remaining boundaries. Failed or blocked required checks leave verification incomplete.

After a complex or unusually costly task, use `$reflect-workflow` only when its evidence gate is satisfied. When changing this workflow's behavioral rules, use [workflow validation](references/workflow-validation.md) to exercise ordinary tasks before treating structural validation as evidence of agent behavior.

## Completion rule

Completion requires passing evidence for the acceptance criteria and required checks on the final changed state, plus resolution of verified in-scope findings. Apply the evidence standard in `$prove-the-work`. A blocked required check leaves verification incomplete; report the implementation and blocker without claiming the task is complete. Optional omissions remain explicit boundaries. Every available workflow layer need not run.
