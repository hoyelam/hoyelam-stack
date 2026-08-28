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

## Pstack alignment review

1. `recall` inspired `$recall-context`; the local version uses runtime-neutral task history and always reconciles against live repository state.
2. `pause safely` and `session pickup` inspired `$checkpoint-work`; the local version preserves authorization boundaries around commits, pushes, and draft pull requests.
3. `create-verification-skill` inspired `$build-verification-harness`; the local version follows each repository's skill convention and keeps unit tests plus full-suite verification in `$prove-the-work`.
4. `reflect` inspired `$reflect-workflow` and the dormant workflow-reflection automation; the local version requires repeated evidence or an explicit preference and does not require a multi-model panel.
5. `blast-radius` strengthened the existing rule to prove important safety facts with executable evidence. It did not justify a duplicate skill because `$investigate-first`, `$prove-the-work`, and `$review-and-resolve` already share that responsibility.
6. `architect` reinforced grounding interfaces and ownership before code. The existing architecture routing remains preferable because iOS work should continue to follow repository documentation, Composable Architecture, and relevant Point-Free skills rather than a universal sketching ceremony.
7. `maintain-verification-skill` is deferred until a real project-local harness shows drift; adding a maintenance workflow before that would encode an unobserved need.
8. Parallel model arenas and autonomous shipping playbooks are not included because prior work supports careful specialist passes, but not a standing preference for model-specific orchestration or automatic merging.

These observations support the workflow; they do not encode private project names, source, or user data.
