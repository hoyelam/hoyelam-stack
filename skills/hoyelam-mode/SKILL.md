---
name: hoyelam-mode
description: "Engineering workflow: investigate, implement, verify, and review non-trivial changes."
---

# Hoyelam Mode

## Scope and depth

Inspect the request, repository instructions, architecture, owning surface, tests, supported builds, runtime harnesses, skills, and environment capabilities. Choose a proportionate route through the workflow below; combine, reorder, narrow, or omit layers when justified. Verification is required for every change; select its depth, not whether to verify. Keep obvious workflow choices brief.

Use more depth for security, privacy, destructive state, money, permissions, signing, concurrency, migrations, releases, and hard-to-reproduce failures. Include user-requested layers unless blocked. State material unavailable, irrelevant, or disproportionate layers as boundaries, never as passing.

Preserve the requested scope: investigation and review stay read-only unless changes are also authorized. For implementation, continue through verification and review. Ask only when a missing decision materially changes the result or requires new authority. When resuming related work, use `$recall-context`; when the user pauses unfinished work, use `$checkpoint-work`.

## Working sequence

1. **Understand.** Read owning source, callers, and relevant architecture guidance. Use `$investigate-first` when cause or ownership is unclear, and `$ios-architecture` when Point-Free architecture can affect an Apple-platform design. State the evidence-backed problem and smallest meaningful boundary.
2. **Define success.** Establish observable acceptance criteria and realistic failure modes before choosing an implementation.
3. **Plan verification.** Discover the project's contract in repository instructions, contributor docs, scripts, or CI. Map each criterion to an exact check or interaction, prerequisites and fixtures, expected result, and evidence. Distinguish required checks from optional evidence. Confirm tools and control paths, run a focused baseline when practical, and reproduce regressions when deterministic. Identify missing coverage, authorized setup, and blockers before dependent implementation. State the plan before editing; one sentence can suffice. Proceed within existing authorization and update the plan as scope or evidence changes without silently weakening criteria. Use `$prove-the-work` when designing or executing a verification contract or when evidence is ambiguous; use its [project verification contract](../prove-the-work/references/project-verification.md) when establishing or repairing project guidance.
4. **Implement.** Make the smallest complete root-cause change that fits the architecture. For larger work, plan small verifiable units and check each before dependent implementation; retain final integration checks. Units do not require separate commits or delegation.
5. **Verify.** Execute the planned checks and capture current evidence suited to the output, including documentation, configuration, libraries, services, scripts, and apps. Re-exercise a regression's original reproduction through the same relevant interface after fixing it; report unavailable proof. Route iOS, macOS, and Electron through `$verify-ios-apps`, `$verify-macos-apps`, and `$verify-electron-apps`. Use `$build-verification-harness` for a missing recurring real-app control path and `$maintain-verification-harness` for drift.
6. **Review and resolve.** Review the complete scoped diff through `$review-and-resolve`, including `$comment-discipline` for touched comments or directives. Use independent review for substantial or risky changes when available and authorized. Validate findings, automatically fix confirmed in-scope issues, and report out-of-scope work separately.
7. **Re-verify.** Rerun checks affected by review fixes on the final state and inspect the revised diff. Repeat review and resolution when new verified issues remain. Retain still-current evidence when nothing relevant changed; do not rerun merely to mark a step done.
8. **Report evidence.** Report the result, tested state, observed outcomes, resolved findings, and concrete remaining boundaries using `$prove-the-work`'s evidence standard.

## Coordination

Use `$orchestrate-project` for substantial work needing ongoing coordination across independently executable units or sessions. The coordinator owns scoped briefs, dependencies, integration, and current evidence. Plan unit verification before delegation, inspect worker results, require unit checks and review, and verify the combined result. Use existing coordination tools or the bundled runtime. Difficulty or multiple steps alone do not justify orchestration; work directly when one agent can reasonably complete and verify the outcome.

For bounded delegation, first decide whether an independent evidence stream would materially improve the decision or elapsed time. Keep framing, discovery, authorization, and integration in the parent. Before assigning work, read [single-task delegation](references/single-task-delegation.md) for scope, briefing, and execution-route rules, including automatic Herdr detection and native fallback. Honor user preferences and available authority.

## Completion rule

Completion requires passing acceptance criteria and required checks on the final changed state, plus resolution of verified in-scope findings. Failed or blocked required checks leave verification incomplete: report the implementation and blocker without claiming completion. Optional omissions remain explicit boundaries; every available layer need not run.

After complex or unusually costly work, use `$reflect-workflow` only when its evidence gate is satisfied. When changing this workflow's behavioral rules, run [isolated workflow exercises](references/workflow-validation.md); structural validation alone does not prove agent behavior.
