# Bundled orchestration runtime

Use this adapter when the project has no suitable coordination records or selects the bundled Python runtime. The CLI maintains records; the agent runtime supplies delegation. The [core playbook](../SKILL.md) governs acceptance, integration, and completion. The store validates bookkeeping, while the coordinator must validate the evidence and overall completion predicate.

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

1. Read [worker-brief.md](worker-brief.md) before creating the first worker brief and [scope-leases.md](scope-leases.md) before assigning the first mutable boundary.
2. A unit must name its goal, writable and forbidden scope, context, acceptance criteria, verification, dependencies, timebox, assignment identity, scope leases, and report shape.
3. Refuse to delegate a unit whose missing context would force a worker to guess.
4. Before starting work, record the worker, thread identity, attempt, and canonical exclusive lease keys:

   ```bash
   python3 <skill-directory>/scripts/orchestrator.py --store <store> unit assign <unit> --worker <worker> --thread <thread> --lease <scope-key>
   ```

5. When subagents are available and authorized, delegate independent ready units concurrently. Otherwise execute the same units sequentially while preserving their boundaries and state.
6. Run one representative unit through implementation and verification before broad fan-out. Correct the brief and unit size from pilot evidence.
7. Prefer a rolling window that refills as units finish. Never allow two workers to hold the same scope lease or write the same worktree, branch, file boundary, simulator state, or mutable external resource concurrently.

## Drain and verify

1. Treat worker completion as an inbox event bound to its stored worker, thread, and attempt. Finish the current critical state update before draining queued reports. Assigned units require all three identity fields, including for late results and retries.

   ```bash
   python3 <skill-directory>/scripts/orchestrator.py --store <store> inbox push <event> --unit <unit> --status <status> --report <report> --worker <worker> --thread <thread> --attempt <attempt>
   ```
2. Inspect every report before changing its unit state. Missing or contradictory evidence becomes a blocked or failed unit, not a pass.
3. Release every assignment with its outcome. A completed attempt must include its revision or artifact identifier; failed, blocked, and cancelled outcomes release their leases and preserve attempt history.

   ```bash
   python3 <skill-directory>/scripts/orchestrator.py --store <store> unit release <unit> --outcome completed --revision <revision> --worker <worker> --thread <thread> --attempt <attempt>
   ```

4. Record verification against the exact revision or artifact identifier. A changed revision invalidates earlier evidence automatically. When a project harness supplied runtime proof, also record its name and revision, doctor status, mapped feature identifiers, and preserved artifact references:

   ```bash
   python3 <skill-directory>/scripts/orchestrator.py --store <store> verification record <unit> \
     --revision <revision> --verdict verified --evidence "<summary>" \
     --harness <verify-skill> --harness-revision <harness-revision> --doctor passed \
     --feature <feature-id> --artifact <artifact-reference>
   ```

   The structured harness fields describe the bundled harness format. For an existing equivalent harness without that schema, omit those flags and put its identity, readiness observations, exercised behavior, and artifact paths in the evidence summary. Do not invent a doctor result. When supplied for a verified verdict, doctor, feature, and artifact fields are required so readiness cannot masquerade as behavior evidence.
5. Use an independent verifier when evidence is judgment-heavy, expensive, security-sensitive, or high impact. A cheap deterministic command may be run by the worker and spot-checked by the coordinator.
6. Park only genuine product decisions or newly required authority as gates. Continue ready work that does not depend on an open gate.
7. Generate status from the store instead of maintaining a narrative progress board by hand.

## Resume and close

1. On a new task or after interruption, run `resume` before creating more work. Treat a durable-store validation error as corruption to repair or restore before any mutation.
2. Reconcile every unit with its durable state, active assignment, thread identity, latest attempt, scope leases, latest report, current revision, and verification verdict.
3. Reuse a known thread only when its role and context still fit the unit. Every retry receives a new stored attempt number and reacquires its leases.
4. Retry according to the observed failure. Cap repeated attempts, then mark the unit blocked or abandoned with evidence instead of looping indefinitely.
5. Close only when every unit is done or explicitly abandoned, no assignment or lease remains active, each done unit has current verified evidence, and every gate is resolved.
6. Report the completion predicate, unit counts, attempts, current assignments and leases, current verification, abandoned work, unresolved boundaries, store path, and worktree state.

Run the CLI with `--help` for unit, inbox, verification, gate, status, resume, and close commands.
