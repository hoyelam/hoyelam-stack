# Instruction simplification — 2026-09-10

Review of all 16 skill entrypoints and the main orientation and delegation documents found most guidance already concise. This round shortened three overlapping coordination documents. Core defaults, reviewer selection, platform procedures, runtime scripts, and earlier evidence were left unchanged.

| Document | Before words | After words |
| --- | --- | --- |
| Orchestrate-project | 633 | 463 |
| Delegation reference | 283 | 189 |
| Codex adapter | 207 | 132 |
| Total | 1,123 | 784 |

The 30.2% reduction removes repeated delegation choices and brief requirements, shortens execution and recovery prose, and keeps Codex guidance focused on runtime mechanics. This is a source word count, not proof of better model comprehension or efficiency.

## Review and acceptance

Before editing, acceptance was defined as clearer wording with the existing delegation discretion, authority, ownership, recovery, and verification requirements preserved. Review compared the complete before/after text and linked guidance. It retained explicit Herdr requirements and fallback behavior, runtime limits, context choice, exclusive writes, current dependency evidence, late-result checks, ownership release, bounded retries, and final integration checks. The optional brief remained an example after review corrected wording that could have made it mandatory. This was self-review.

`./scripts/validate.sh` passed before and after the instruction edits: 74 tests, zero failures, zero skips; 16 skills, 10 agents, and 3 automation packs validated. Documentation reference checks and `git diff --check` also passed. No new tests merely asserting instruction strings were added.

## Isolated workflow exercise

A fresh ephemeral Codex session implemented the shipped `modules` task in `/private/tmp/stack-clarity-a1`, using the configured model, workspace sandbox, and automatic approval review. It received the ordinary task prompt and project-local copies of the final skills, with checker details and starting fingerprints outside its project. The parent confirmed every copied skill matched the final source.

The agent read the simplified orchestration and delegation documents and chose delegation. The CLI could not start a worker (`no thread with id`); it then recorded direct ownership, implemented both domains and the CLI, added meaningful tests, and verified integration. A preliminary Git status command failed because the fixture was not a Git repository; the subsequent instruction read succeeded.

The independent checker returned `passed`: **20 tests, zero skips**, domain assertions, multiple CLI inputs, invalid-input handling, and allowed-file scope all passed. The documented order returned 725 cents with fulfillment `[2, 1, 1]` and zero remaining pen/book stock. The parent reviewed the implementation, assertions, command activity, and final answer. No user intervention was needed.

The [machine-readable record](instruction-simplification-2026-09-10.json) retains before/after instruction hashes, fixture version, request, starting and final product fingerprints, actual commands, results, elapsed time (189.35 seconds), and available token usage. The starting state includes the preceding task's uncommitted changes; its historical evidence was not rewritten. Raw logs and snapshots are under `.work/instruction-simplification/` and may expire.

This diagnostic sample verifies the observed task outcome and direct fallback. It does not prove completed native delegation, every context-fork strategy, Herdr execution, or interrupted recovery; those instructions received source review only. Inherited configuration, shared caches, and unverified child-token coverage prevent a controlled performance comparison.
