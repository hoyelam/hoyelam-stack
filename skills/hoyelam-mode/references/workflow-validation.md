# Validate agent behavior

Use this when changing behavioral guidance. Package validation proves structure and helper behavior; actual tasks show how agents use the instructions. Select exercises affected by the change and keep their scope proportionate.

## Design the observation

Define success in terms of outcomes: correct behavior, meaningful proof, scope preservation, useful delegation, focused repairs, and honest blocked status. A correct alternative approach is acceptable. Do not grade adherence to a prescribed phase order or count skill invocations as quality.

For efficiency comparisons, use the same ordinary requests, starting projects, model/configuration, and tool availability for each variant. Keep scoring criteria, variant identities, expected fixes, and other workers' results outside candidate workspaces. Inspect actions and artifacts instead of accepting a worker's claimed compliance. Keep benchmark fixtures separate from production data.

## Reusable local projects

From this repository, use `python3 scripts/workflow_exercises.py prepare --case CASE --stack STACK_PATH --dest NEW_PROJECT_PATH`. Run `--help` for the supported arguments. The helper creates an ordinary project with a local copy of the selected skills and emits its task prompt. It keeps initial fingerprints in a sibling manifest outside that project. Use neutral project paths and pass only the emitted prompt to the worker; do not provide the checker or manifest.

| Case | Observable concern |
| --- | --- |
| `docs` | A small documented command is corrected and actually invoked without expanding scope. |
| `parser` | A regression is fixed with meaningful tests and real CLI behavior. |
| `parser-blocked` | Available work succeeds while a missing required external check remains blocked. |
| `modules` | Independent domain work in one repository is integrated and verified. |
| `harness` | One broken control path is repaired without changing the product or auditing an unrelated unavailable feature. |

Run each worker in its own project using authorized local actions. In Codex, use a fresh session with the supported workspace sandbox, preserve the configured model, and capture task-local JSON events and the final answer outside the candidate workspace. Do not disable safeguards to make an exercise pass. Record tool/runtime limitations, including unavailable native delegation.

After the worker stops, run `python3 scripts/workflow_exercises.py check --case CASE --project PROJECT_PATH`. This independently exercises the artifact and checks scope. Review the actual diff, assertions, final response, and tool activity as well: a checker alone cannot establish useful delegation, truthful reporting, or actions outside its observed workspace. Observe worker assignments and integration for the modules case; inspect selected coverage for harness repair.

For review-and-resolution changes, inspect a supported finding, resulting fix, and affected rerun. Distinguish naturally found issues from deliberately supplied findings; do not invent a finding to fill a workflow stage. Pause/resume or runtime-specific changes may need additional targeted tasks beyond the bundled projects.

## Retain and compare evidence

Record source revision and instruction hashes, fixture version, requests, starting and final state, executed commands, observed results, and artifact locations. Keep raw task logs outside portable instructions; retain sanitized durable observations and note when temporary logs may expire.

Capture elapsed time, available input/output/cache token usage, redundant calls, errors, and user interventions. Distinguish total work from elapsed time and cached usage from uncached usage. Report unavailable metrics as unobserved. Compare correctness and evidence quality alongside cost, and disclose shared environment or cache effects. One run per case is a diagnostic sample, not a reliable speed ranking.

After fixes, rerun affected checks and exercises on the final guidance. Preserve failures and still-current evidence. Small synthetic projects cannot establish reliability across platforms or agents, and fewer instruction words alone do not prove better task performance.
