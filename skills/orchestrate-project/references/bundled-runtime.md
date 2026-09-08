# Bundled orchestration runtime

Use this optional store when automated assignment identities, exclusive leases, inbox records, or recovery help the task. The CLI manages records; the selected agent tools execute work. The [core playbook](../SKILL.md) governs acceptance and integration. Store validation proves bookkeeping, while the lead assesses evidence and the overall outcome.

## Commands

Run `python3 <skill-directory>/scripts/orchestrator.py --store <store> --help` and the relevant subcommand's help for exact flags. Successful calls return JSON. Keep one authoritative store, normally under `.hoyelam/orchestrate/<project>`, and keep scratch state ignored unless the user requests it in version control.

Initialize the goal and instructions, then add independently verifiable units:

```bash
python3 <skill-directory>/scripts/orchestrator.py --store <store> init --goal "<goal>" --done "<predicate>" --standing-order "<constraint>"
python3 <skill-directory>/scripts/orchestrator.py --store <store> unit add <unit> --goal "<outcome>" --scope "<boundary>" --acceptance "<criteria>" --verify "<checks>"
```

Repeat `--standing-order` or `--depends-on` when needed. Before assigning a mutable boundary, read [scope-leases.md](scope-leases.md). Record ownership before starting writes:

```bash
python3 <skill-directory>/scripts/orchestrator.py --store <store> unit assign <unit> --worker <worker> --thread <session> --lease <scope-key>
```

Use the returned attempt number. Include worker, session, and attempt on reports and release operations so late results cannot replace a current assignment. Repeat `--lease` for each owned boundary.

```bash
python3 <skill-directory>/scripts/orchestrator.py --store <store> inbox push <event> --unit <unit> --status <status> --report "<report>" --worker <worker> --thread <session> --attempt <attempt>
python3 <skill-directory>/scripts/orchestrator.py --store <store> inbox drain
python3 <skill-directory>/scripts/orchestrator.py --store <store> unit release <unit> --outcome completed --revision <artifact> --worker <worker> --thread <session> --attempt <attempt>
python3 <skill-directory>/scripts/orchestrator.py --store <store> verification record <unit> --revision <artifact> --verdict verified --evidence "<observations and artifact paths>"
python3 <skill-directory>/scripts/orchestrator.py --store <store> unit set <unit> --state done
```

Inspect reports before updating acceptance. Release every assignment with its actual outcome; failed, blocked, and cancelled attempts also release leases and retain history. Completed attempts enter verification and require an artifact identity. Record evidence before marking a unit done. Evidence is bound to the exact revision; changed revisions require current verification. Use `verification check <unit>` to inspect it and `status` for generated progress.

## Optional harness fields

When using the bundled harness format, add `--harness <name> --harness-revision <revision> --doctor passed --feature <id> --artifact <path>` to a verified receipt. The runtime requires doctor, feature, and artifact fields together for that format. Repeat feature and artifact flags as needed. Never invent a doctor result.

For an equivalent harness with different conventions, omit those flags and include its identity, readiness observations, exercised behavior, and preserved artifact paths in `--evidence`.

## Recovery and close

Run `resume` after interruption, reconcile live assignments and dependencies with the returned state, and repair or restore corrupt records before mutation. A retry gets a new attempt and reacquires released leases; the lead diagnoses the cause and bounds retries.

Use `gate add` and `gate resolve` for actual missing decisions or authority. Continue work independent of those gates. `close` requires every unit done or explicitly abandoned, current verified evidence for done units, no active assignment or lease, and resolved gates. It closes bookkeeping; abandoned required work still leaves the original goal incomplete.
