---
name: investigate-first
description: Investigate a request, defect, regression, or unfamiliar subsystem before implementation by locating the real code, tracing origin and callers, and producing an evidence-backed boundary.
---

# Investigate First

## Investigation

1. Translate the request into expected behavior, observed behavior, constraints, and a falsifiable completion condition.
2. Locate the actual repository root before assuming the supplied working directory is correct.
3. Read applicable instructions, architecture documents, execution plans, and local verification commands.
4. Find the owning source, direct callers, state transitions, external boundaries, tests, fixtures, and adjacent implementations.
5. Inspect relevant version history and blame when behavior may be a regression or an architectural choice.
6. Reproduce or observe the symptom when safe. Prefer logs, traces, crash reports, state readback, or a minimal script over speculation.
7. Trace the behavior backward until the root cause or unmet requirement is supported by evidence.
8. Identify the smallest feature boundary that can be changed and verified independently.
9. Identify the one or two facts the proposed boundary is safe because of. Prove each as far as practical with source evidence, a focused test or script that runs real code, or the running artifact. Mark unproved facts explicitly.

## Output

Return:

1. Expected versus observed behavior.
2. Root cause or strongest remaining hypothesis, with evidence.
3. Owning files, symbols, callers, and tests.
4. Blast radius, architecture constraints, and the proved or unproved safety facts.
5. Proposed boundary and verification plan.
6. Unknowns that would materially change the implementation.

Do not edit application code when the request is investigation-only.
