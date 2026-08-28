---
name: orchestrate-project
description: Coordinate a project-scale engineering program that spans multiple independent units or sessions with durable state, explicit worker briefs, revision-bound verification, and resumable progress. Do not use for work one agent can finish directly.
---

# Orchestrate Project

## Route deliberately

1. Use this skill when the requested outcome spans multiple independently executable units, is expected to outlive one task context, or explicitly assigns ongoing coordination.
2. Keep ordinary features, fixes, investigations, and single-session autonomous work in `$hoyelam-mode`.
3. Collapse orchestration when one agent can reasonably complete and verify the work directly. The state store and delegation ceremony must earn their cost.
4. Preserve the user's authorization boundaries. Coordination does not authorize publishing, deployment, destructive actions, messages, purchases, or unrelated scope.

## Frame the program

1. Define a countable completion predicate and the evidence required for each completed unit.
2. Split work by independently writable and verifiable boundaries. Give each boundary one writer at a time.
3. Record standing constraints before delegation so every new or resumed worker receives the same instructions.
4. Initialize durable state with the bundled runtime:

   ```bash
   python3 <skill-directory>/scripts/orchestrator.py --store .hoyelam/orchestrate/<project> init --goal "<goal>" --done "<predicate>" --standing-order "<constraint>"
   ```

5. Keep `.hoyelam/` ignored unless the user explicitly wants the coordination record committed.

## Brief and execute units

1. Read [references/worker-brief.md](references/worker-brief.md) before creating the first worker brief.
2. A unit must name its goal, writable and forbidden scope, context, acceptance criteria, verification, dependencies, timebox, and report shape.
3. Refuse to delegate a unit whose missing context would force a worker to guess.
4. When subagents are available and authorized, delegate independent ready units concurrently. Otherwise execute the same units sequentially while preserving their boundaries and state.
5. Run one representative unit through implementation and verification before broad fan-out. Correct the brief and unit size from pilot evidence.
6. Prefer a rolling window that refills as units finish. Never allow two workers to write the same worktree, branch, file boundary, simulator state, or mutable external resource concurrently.

## Drain and verify

1. Treat worker completion as an inbox event. Finish the current critical state update before draining queued reports.
2. Inspect every report before changing its unit state. Missing or contradictory evidence becomes a blocked or failed unit, not a pass.
3. Record verification against the exact revision or artifact identifier. A changed revision invalidates earlier evidence automatically.
4. Use an independent verifier when evidence is judgment-heavy, expensive, security-sensitive, or high impact. A cheap deterministic command may be run by the worker and spot-checked by the coordinator.
5. Park only genuine product decisions or newly required authority as gates. Continue ready work that does not depend on an open gate.
6. Generate status from the store instead of maintaining a narrative progress board by hand.

## Resume and close

1. On a new task or after interruption, run `resume` before creating more work.
2. Reconcile every unit with its durable state, latest report, current revision, and verification verdict.
3. Retry according to the observed failure. Cap repeated attempts, then mark the unit blocked or abandoned with evidence instead of looping indefinitely.
4. Close only when every unit is done or explicitly abandoned, each done unit has current verified evidence, and every gate is resolved.
5. Report the completion predicate, unit counts, current verification, abandoned work, unresolved boundaries, store path, and worktree state.

Run the CLI with `--help` for unit, inbox, verification, gate, status, resume, and close commands.
