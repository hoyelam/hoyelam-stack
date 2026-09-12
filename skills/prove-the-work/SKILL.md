---
name: prove-the-work
description: Clarify acceptance checks or assess uncertain verification evidence.
---

# Prove The Work

Establish what would prove the requested outcome, run the relevant checks, and report what the evidence supports. Scale the work to the changed behavior and risk; a prose edit may need only source comparison and link checks.

## Choose the proof

Before editing, identify observable success and the checks that could disprove it. Start with the project's existing verification commands and the original reproduction for a bug. Distinguish required acceptance checks from optional evidence using the request, project contract, and actual risk. A short explanation is enough for routine work; use a detailed plan only when dependencies or uncertainty make it useful.

Choose evidence at the affected boundary: focused behavior tests, a real command invocation, a changed user path, or inspection of the produced output. Include realistic failure cases and adjacent behavior when they could expose a regression. Prefer existing tools and available verification skills; creating a harness is useful only when a recurring verification gap warrants it. Read the [project verification contract](references/project-verification.md) when establishing or repairing a project's verification guidance.

Check prerequisites before relying on a verification path. Reproduce the original failure before fixing it when a cheap deterministic route exists, and report unavailable reproduction. For delegated work, agree on evidence each unit should return and verify the combined result; isolated passes do not prove integration.

## Run and assess

Run required and selected checks, inspect their actual output, and re-exercise a bug's original reproduction through the relevant interface after fixing it. Add tests when they provide meaningful behavioral coverage, not merely to mirror implementation. Use snapshots when rendered output is the contract. Adapt additional checks to new evidence without silently weakening acceptance criteria.

Tie evidence to the final changed state, including uncommitted changes. Rerun checks affected by code, fixture, dependency, configuration, generated artifact, or review changes. Retain evidence for unaffected claims; do not repeat checks solely to complete a workflow step. Rebuild or restart when stale artifacts could conceal the result. CI evidence must match the relevant revision; a local pass does not imply CI passed.

## Evidence standard

Report the outcome, tested state, checks performed, observed results, and material gaps. Include commands or interactions, exit status, test counts, and evidence paths when needed to substantiate the result or allow a handoff. Keep routine evidence in the task report; use existing records when evidence must survive delegation or a pause.

Use `passed`, `failed`, `blocked`, or `not run` for check results. A pass requires the intended checks to have actually executed and matched the expected result. Zero discovered tests, unexpected skips, a started command, a green exit without expected output, and a reviewer assertion do not prove the behavior.

Diagnose failures before retrying. Do not delete or weaken assertions, widen tolerances, skip checks, or change expected behavior merely to obtain a pass. Preserve flaky attempts and report the unresolved failure unless its cause is fixed or evidence establishes an unrelated baseline issue. An unrelated baseline failure remains visible and cannot be reported as a passing required check.

Compilation proves syntax and linkage; tests and runtime checks prove only the behavior they exercise. Never present proxy evidence as a stronger pass. Completion requires passing acceptance criteria and required checks on the final changed state. Failed or blocked required checks leave verification incomplete: continue independent authorized work and report the blocker and next action without claiming completion. Optional checks remain optional; disclose material limitations rather than accounting for every tool or layer not used.
