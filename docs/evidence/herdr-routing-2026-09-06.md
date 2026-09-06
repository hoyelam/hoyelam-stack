# Automatic Herdr routing verification — 2026-09-06

Base: `6a3a1020ab4dc3574ba7d81f0a6de0850beaccc8` plus the instruction changes identified below.

## Acceptance and checks

Select Herdr for useful, authorized delegation when the managed environment, CLI, and caller/session checks pass. Preserve explicit native/no-delegation preferences, native/direct fallback for unavailable automatic detection, and a reported blocker for unavailable explicitly required Herdr. Keep the current model as lead; worker model configuration remains unchanged.

Package validation and deliberate source review cover entry-point consistency and fallback policy. A live isolated bug-fix exercise covers actual automatic tool selection and integration. This is a targeted exercise, not a reliability claim across all agents or environments.

## Review and package evidence

`./scripts/validate.sh` passed after the workflow guide fix: 16 skills, 10 agents, 3 automation packs, 44 tests, no skips. `git diff --check` passed.

Independent reviewer `routing-review`, attempt 1, pane `w9:p5`, Codex session `01a07818-fb73-7b80-a76e-b00d1b6e8ab7`, inspected the three skill changes read-only and ran validation (44 tests passed). It found one stale opt-in rule in `docs/workflow.md:35`. The lead aligned it with the owning rule and reran validation. No other supported correctness findings were reported. No code comments were introduced.

Live bootstrap: `HERDR_ENV=1`; `command -v herdr` found the installed CLI. After loading `herdr --skill`, `herdr --help`, `herdr pane`, and `herdr agent`, the lead ran `herdr pane current --current` and `herdr pane layout --current`, each with a 10-second subprocess timeout. Sandbox socket access failed with PermissionDenied; the permitted elevated retry resolved caller `w9:p2` in `w9:t1`. A sibling pane was created with `--no-focus` and the same cwd. `herdr agent start routing-review --kind codex --pane w9:p5` returned ready; its terminal identified `gpt-6-astra medium`. The lead submitted the review via `herdr agent prompt` and inspected its actual report via `herdr agent read`.

## Isolated workflow exercise

Fixture: `/private/tmp/herdr-routing-exercise-3ipygy6b`. Starting source is retained as `price.py.before`; README specifies a bulk discount at 10 items and `python3 -m unittest discover -v`. The lead independently ran the baseline: 3 tests, one failure (`total(10)` returned 60 instead of 50).

Ordinary request to the worker: fix the pricing boundary according to README, run tests, apply current hoyelam-mode, and obtain one independent read-only review. The request did not specify the delegation runtime. Writes are restricted to the fixture and one read-only helper is allowed. The worker receives no expected route or scoring criteria in this assignment, though it retains prior review context.

Observed automatic selection: the worker read the updated skill, reproduced and fixed the boundary, passed all three tests, loaded the installed Herdr instructions, and checked the current pane with a 10-second timeout. After a permitted sandbox retry it resolved its own `w9:p5`, selected Herdr without a runtime instruction in the task, split a sibling pane with `--no-focus`, and started `price-review-a2` in `w9:p6`. The helper used the configured Astra model. The original startup returned `agent_not_ready` at a directory-trust prompt; the worker inspected it and reported the blocker without approving it. After the screen independently cleared, the lead observed idle/readiness and resumed the worker using the same helper.

The lead independently reran `python3 -m unittest discover -v` on the changed fixture: all three tests passed. The source diff changes only `quantity > 10` to `quantity >= 10`.

Limitations: explicit native/no-delegation overrides and absent/unreachable Herdr fallback were reviewed as instruction contracts, not executed in separate environments. The exercise required independent review to make delegation useful and retained the worker’s prior routing-review context; it was not a blind comparison against the old instructions. This verifies the live automatic route for this task, not universal selection reliability. No model settings or published release were changed.

The helper returned `PASS` with no findings and independently ran all three tests successfully. Helper Codex session: `01a0781c-9825-77c2-bb46-3a63c5ae6cd0`. The exercise coordinator inspected its terminal report and checked that the source/test hashes remained unchanged. Its durable record and preserved reviewer output are in the temporary fixture (`review-record.md` and `reviewer-report.txt`). The lead separately inspected the helper’s actual report before accepting it.

## Instruction SHA-256

- `skills/hoyelam-mode/SKILL.md`: `d24120667c9022938b8798ff31b52fb518fecf0e604bc11f24f1a36f45d17880`
- `skills/hoyelam-mode/references/herdr-delegation.md`: `684a9aa9a1a8d6e73a9fee316b89bc1b7be5fd784c436716949e43e2311871a6`
- `skills/orchestrate-project/SKILL.md`: `30d8e3c399f80f1fe868b141600926380f39075d3313c53398600cf8214cebce`
- `docs/workflow.md`: `13b59c8e72e08794940bf8a3634296c87a7d7668f7457979373a6d33c20e6c03`
