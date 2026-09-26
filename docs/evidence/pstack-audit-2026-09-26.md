# Hoyelam-stack / PStack audit — 2026-09-26

The current stack already covers investigation, verified completion, scoped review, app harnesses, continuity, and optional orchestration well. This audit fixes one reproduced installer defect and adds three focused pieces of guidance to existing skills. It introduces no new skills, mandatory workflow phases, model assignments, or automatic shipping authority.

## Compared state

The local starting point was `bd457986fe611366ee9acad6e876db0f12f9b3d6` plus existing uncommitted work from the September 14 routing change. That work makes Hoyelam Mode optional and explicit-only; it was preserved. All 16 installed skill links resolve to the maintained source repository.

Upstream was [cursor/plugins at ecc249f1e306fc64ddf83c7bed16cacf7c2239db](https://github.com/cursor/plugins/tree/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack), committed September 25. Source reads used GitHub CLI. Scope covered every local skill entrypoint, relevant supporting guidance, the installer and repository checks, and targeted PStack sources. It was not an exhaustive audit of every helper implementation or an app runtime test.

## Findings and decisions

| Finding | Evidence and change |
| --- | --- |
| **Installer rejects equivalent repository paths.** | Existing links use the compatibility alias, while the maintained repository has a canonical path. The installer compared link text, so rerunning from the other path failed. Two regression cases reproduce this with aliases and valid relative links. It now compares filesystem identity while still requiring an existing symlink; unrelated directories, unrelated symlinks, and dangling links remain conflicts. Existing links are preserved. |
| Review guidance under-specifies consumers outside symbol searches. | [PStack blast-radius](https://github.com/cursor/plugins/blob/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack/skills/blast-radius/SKILL.md) explicitly traces serialized data, downstream consumers, lifecycle order, and pinned dependency behavior. `review-and-resolve` now asks for these checks when a contract boundary changes, with a focused attempt to disprove the safety assumption. |
| Repeated failed fixes lack an explicit change-of-hypothesis trigger. | [Attack the Premise](https://github.com/cursor/plugins/blob/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack/skills/principle-attack-the-premise/SKILL.md) challenges assumptions shared by failed attempts. `investigate-first` now asks for a distinguishing observation before another variation. Actor comparisons apply when load or ownership is uneven; they are not a mandatory ritual for every bug. |
| Performance proof is less explicit than correctness proof. | PStack's [performance playbook](https://github.com/cursor/plugins/blob/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack/skills/poteto-mode/playbooks/perf-issue.md) centers measured baseline and final results. A conditional reference under `prove-the-work` now covers matched workloads, noise, cold versus warm state, correctness, tradeoffs, and honest limits. Existing platform profilers remain the owners of instrumentation. |

The first finding is an executable defect. The other three are guidance improvements supported by a concrete coverage difference and the exercises below; they are not claims that the old instructions always produced bad decisions.

## Practices retained

- Optional focused skills and the explicit-only personal mode. PStack's [main workflow](https://github.com/cursor/plugins/blob/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack/README.md) uses required playbooks and wider skill chains; those would conflict with the current local preference for task-led methods.
- Model and delegation discretion. PStack's [architect](https://github.com/cursor/plugins/blob/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack/skills/architect/SKILL.md) and [interrogate](https://github.com/cursor/plugins/blob/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack/skills/interrogate/SKILL.md) prescribe several model perspectives. The local stack already supports independent review and alternative designs when useful; this audit supplies no evidence for making them universal.
- Existing regression and reflection guidance. PStack's [TDD](https://github.com/cursor/plugins/blob/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack/skills/tdd/SKILL.md) and [structural lessons](https://github.com/cursor/plugins/blob/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) overlap the current preference for meaningful reproductions and executable checks. The installer fix follows this approach without adding another rule to an agent prompt.
- Existing bounded recall, checkpoints, harness ownership, and final-state verification. These remain more useful than expanding the catalog for upstream feature parity.

## Verification

The baseline repository check passed 74 tests. Both new equivalent-path regression tests failed against the original installer and passed after the fix. The final helper suite passed 77 tests without failures or skips and validated 16 skills, 10 agent briefs, and three automation packs. The three changed skills also passed the skill-creator validator.

Three fresh native workers received ordinary requests in separate synthetic Python projects, their relevant local skills, and no expected findings or scoring criteria. They inherited the configured model without an override and had no parent conversation history. Application and skill files were read-only; scratch evidence was allowed in `.work/`. These exercises were selected under the repository's behavioral-validation requirement, informed by PStack's [evaluation playbook](https://github.com/cursor/plugins/blob/ecc249f1e306fc64ddf83c7bed16cacf7c2239db/pstack/skills/poteto-mode/playbooks/eval.md).

| Exercise | Observation |
| --- | --- |
| Contract review | The worker ran a passing unit test, then reproduced a `KeyError` in a separate CLI consumer of the changed JSON response. It reported the actual regression and left source untouched. The parent independently reproduced both results. |
| Repeated failed timeouts | The worker reproduced assignments of 12/0/0 across timeouts 1, 5, 10, and 20. A scratch experiment distributed independent jobs 4/4/4 and completed all 12. It distinguished one-window backlog from an unproven indefinite stall. The parent independently reproduced the skew and inspected the experiment evidence. |
| Performance comparison | The worker identified mismatched saved workloads and reported matched benchmark runs and one passing correctness test. Its evidence-saving tool call was interrupted, so those reported timings are not the retained measurement record. The parent recorded equal one-million-item workloads in alternating implementation order: 14 samples per implementation, medians 10.7685 ms and 1.49977 ms, with one passing correctness test. This proves only the synthetic integer aggregation result. |

The [machine-readable record](pstack-audit-2026-09-26.json) identifies the source, instruction and fixture hashes, checks, outcomes, and evidence limitations. Raw task-local logs and disposable projects are outside portable guidance and may expire. The standalone validator initially lacked PyYAML; a task-local installation supplied it without changing repository dependencies.

The performance worker needed two parent interventions after tool calls stalled: a bounded retry and a stop after the parent retained direct measurements. Its partial execution is not a clean autonomous workflow pass. No user intervention occurred within the synthetic tasks. All initial application and skill file hashes remained unchanged.

These are diagnostic samples of the revised guidance, not a blinded before/after comparison. They establish exercised behavior and scope preservation, not improved model reliability, lower token cost, or faster delivery. Token usage and worker elapsed times were not measured. A larger real-project comparison is the useful next evidence if further workflow expansion is considered.
