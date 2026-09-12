# Design evidence

The first version reflects recurring patterns from prior engineering tasks without copying project-specific details:

1. Supplied workspaces sometimes contained several repositories, so repository discovery must precede source inspection.
2. Crash diagnosis improved when stack evidence was connected to the change that introduced re-entrant layout behavior.
3. A focused regression test was useful, but the full suite and rebuilt application caught a wider class of failures.
4. Repeated interaction against the live application provided stronger crash-fix evidence than compilation or a single click.
5. Process liveness, logs, persisted state, and crash-report directories supplied independent runtime confirmation.
6. Draft branches and pull requests preserved unfinished work without implying it was ready to merge.
7. Permission, signing, target, and entitlement behavior required production-representative builds rather than package tests alone.
8. Resuming older work was safer when prior decisions were reconciled with the live branch and worktree instead of trusting conversation memory alone.
9. Interrupted implementations benefited from draft-safe checkpoints that preserved work without presenting it as complete.
10. Real application verification repeatedly required repository-specific launch, control, evidence, and cleanup knowledge that should be reusable rather than rediscovered.
11. The most valuable workflow additions came from repeated friction and explicit corrections, while one-off project facts did not belong in global instructions.
12. Apple application work repeatedly required Simulator or macOS interaction, Xcode test evidence, signing or entitlement checks, and rebuilt-artifact verification.
13. Electron work needs separate proof across Chromium renderer state, main-process behavior, native desktop surfaces, packaging, and persisted side effects.
14. The workflow is an explicit preference rather than a fixed sequence: agents should inspect available repository guidance, tooling, and evidence surfaces, then select proportionate layers without weakening safety or overstating verification.
15. Personal response-format preferences belong in user-level skills or instructions rather than the portable engineering stack.
16. Single-task delegation is useful for bounded evidence streams, but parent-owned metadata discovery and integration prevent duplicated orientation and contradictory conclusions.
17. A control CLI, indexed feature map, and explicit maintenance pass turn repository-specific runtime knowledge into testable infrastructure instead of prose that silently drifts.
18. Cold-read web pilots showed that dormant applications fail for distinct product, toolchain, and environment reasons. Useful harnesses preserve that distinction, bind teardown to process birth identity, and prove semantic locators against rendered state.

## Pstack alignment review — historical 2026-09-05

The [orchestration playbook](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/orchestrate.md) and [mode routing](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) were inspected on 2026-09-05. The adaptation inspected on that date kept scoped briefs, a representative pilot, rolling delegation, queued result handling, continuous integration, revision-bound evidence, and restart recovery. Verification governs unit acceptance and the final program outcome. Existing project records can carry the contract; the bundled runtime remains available. Pstack’s specific cloud placement, model choices, stack tooling, and shipping authority are not requirements of this method.

1. `recall` inspired `$recall-context`; the local version uses runtime-neutral task history and always reconciles against live repository state.
2. `pause safely` and `session pickup` inspired `$checkpoint-work`; the local version preserves authorization boundaries around commits, pushes, and draft pull requests.
3. `create-verification-skill` inspired `$build-verification-harness`; the local version follows each repository's skill convention and keeps unit tests plus full-suite verification in `$prove-the-work`.
4. `reflect` inspired `$reflect-workflow` and the dormant workflow-reflection automation; the local version requires repeated evidence or an explicit preference and does not require a multi-model panel.
5. `blast-radius` strengthened the existing rule to prove important safety facts with executable evidence. It did not justify a duplicate skill because `$investigate-first`, `$prove-the-work`, and `$review-and-resolve` already share that responsibility.
6. `architect` reinforced grounding interfaces and ownership before code. The existing architecture routing remains preferable because iOS work should continue to follow repository documentation, Composable Architecture, and relevant Point-Free skills rather than a universal sketching ceremony.
7. `maintain-verification-skill` informed `$maintain-verification-harness`; the local version is product-neutral, changes only harness-owned files, does not impose a fixed cadence, and preserves external-action authorization boundaries.
8. Pstack's orchestrator demonstrated a real gap between routing one task and coordinating a program. `$orchestrate-project` adopts durable units, standing orders, inbox events, revision-bound verification, gates, generated status, pilot-first scaling, and restart recovery without Graphite, PR landing, model-specific routing, or automatic shipping.
9. Pstack's coordinator, brief, and context-guard guidance supports parent-owned synthesis and exclusive writable scope. The local stack adds a Codex adapter, a bounded direct-task router, and durable assignment attempts without vendor-specific execution assumptions.

These observations support the workflow; they do not encode private project names, source, or user data.

## Flexible baseline — 2026-09-07

The user explicitly prefers selectable skills and tools, strong verification, and agents with freedom to choose an efficient execution path. The lead should actively orchestrate substantial independent work, including within one repository. Codex is the preferred runtime; exact model names, context sizes, and arbitrary child-count ceilings do not belong in the portable core.

The resulting design removes the task classifier and mandatory skill chains, centralizes personal defaults, shares continuity records, makes harness maintenance scope explicit, and retains optional platform and orchestration tools. Repeated source research gains a revision-aware cache helper. Reflection considers deletion, user interventions, and resource use as well as missing capabilities.

Pstack's evaluation and project verification ideas remain useful. Agent-stuff's source cache and human-centered session analysis informed the optional research helper and reflection guidance. Superpowers' compulsory invocation methodology was not adopted. These are adaptations; helper implementations are maintained here and must pass their own checks.

The [flexible baseline verification record](evidence/flexible-baseline-2026-09-07.md) records package checks, isolated Codex outcomes, observed delegation, continuity, and context measurements. Shorter source text alone does not establish better task performance.

## Delegation discretion — 2026-09-10

The user clarified that the model should decide when delegation helps. Current guidance therefore replaces the earlier preference for active orchestration of substantial work with model judgment about direct work, delegation, reviewer selection, concurrency, and handoff context. Ownership and final-state verification remain strict; coordination tooling remains optional.

The [verification record](evidence/delegation-discretion-2026-09-10.md) documents final-source package checks and isolated task outcomes, along with an additional native-tool observation whose implementation was blocked by automatic approval review. It does not claim an efficiency improvement or completed native delegation evidence.

The subsequent [simplification round](evidence/instruction-simplification-2026-09-10.md) shortened three overlapping coordination documents while preserving their requirements. It records source review, package checks, and a fresh module-integration exercise; shorter wording alone does not establish better model performance.

## Astra-first reassessment — 2026-09-12

The [reassessment record](evidence/astra-reassessment-2026-09-12.md) covers clearer discovery triggers, aligned invocation metadata, conditional reading, explicit-only alternatives, and implementation persistence. It separates portable changes from installed personal settings and records passing local checks, 14 expected functional workflow outcomes across Astra and Sol, and an explicit Apple-router smoke test. Mixed timing and bounded workflow deviations prevent claiming a universal efficiency improvement or perfect instruction adherence.
