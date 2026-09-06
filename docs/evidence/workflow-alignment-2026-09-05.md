# Workflow alignment verification, 2026-09-05

This change makes verification govern orchestration and keeps the personal workflow independent of a particular coordination runtime, app driver, or CI service. It adds focused iOS and macOS entrypoints sharing the existing Apple guidance. The bundled runtime and diagnostics remain available.

## Acceptance and verification plan

Before implementation, the parent selected package/link validation, existing helper tests, skill validation, isolated installation, independent instruction review, and an isolated implementation exercise. Acceptance requires prominent orchestration with scoped ownership and integrated evidence, compatible existing project tools, proportional platform and automation checks, and explicit required-check gates.

- `./scripts/validate.sh`: passed, 16 skills, 10 agents, 3 automation packs; 44 tests passed with no skips.
- `quick_validate.py`: all nine changed or new skill packages passed using the cached PyYAML environment.
- `validate_plugin.py`: plugin validation passed.
- Isolated `install-local.sh`: all 16 skill links resolved to source, including the new platform entrypoints; a second run reused all links.
- `git diff --check`: passed.

The helper scripts and existing tests were unchanged. Structural tests do not prove agent behavior.

## Independent review

A read-only reviewer inspected the complete changed instructions, metadata, and new references. It confirmed one inconsistency: the platform guide still required bundled receipt fields for every existing verification skill. The parent changed that rule to accept equivalent project evidence; the reviewer re-read it and found no remaining supported instruction findings. The platform writer also corrected claims that could imply external platform tools ship inside this plugin.

## Behavioral exercise

An independent worker received an ordinary two-unit receipt request, the source workflow, and an isolated project with an existing `progress.json`. It implemented percentage discounts and optional item counts. The fixture deliberately included an unavailable required deployment check; that was a constructed verification gate, not a discovered infrastructure incident.

The worker retained the existing record format, added scoped verification evidence, and reported the program as `verification_blocked` despite passing local checks. It used direct sequential execution and self-review for the small task. This exercises reuse of project records and honest completion handling, not multi-agent fan-out.

The parent reconstructed the final files in a second temporary workspace and observed:

- Final suite: 16 tests passed, no skips.
- Ten independent acceptance checks passed, covering compatibility, discounts, boundaries, count output, and iterable input.
- Existing CLI still printed `Total: 5`, exit 0.
- Required deployment check still exited 78 with its original unavailable-staging message.
- The final tests run against the starting implementation failed with 14 errors, exit 1, detecting the missing APIs.
- Project instructions, original CLI, and deployment check remained byte-identical to their starting state.

The [replay record](workflow-alignment-2026-09-05.json) preserves instruction hashes, starting and final fixture files, worker-authored records/logs, independent replay commands, and observed outputs. Planning-before-editing is worker-reported; a task-local activity timeline was not independently inspected. An initial automatic approval rejection of the fixture edit was resolved by supplying the original user request and repository-required isolated-validation authority; the same patch retry succeeded.

A separate read-only evidence review verified all 44 recorded instruction hashes and seven final artifact hashes, confirmed the protected files were unchanged, and independently replayed the 16 tests, ten acceptance checks, CLI result, deployment blocker, and 14-error starting-source run in memory. It found no unsupported narrative claims or remaining findings.

## Limits

The fixture is a small sequential Python project. It cannot establish reliability for large programs, concurrent worker queues, actual restart recovery, or production iOS, macOS, and Electron applications. No real platform app was exercised. The bundled runtime's assignment, stale-evidence, and closure behavior remains covered by the existing repository tests.

No comparison against an earlier workflow variant was run. Worker-authored logs and ordering claims are distinguished from independent replay. The earlier workflow exercise remains historical evidence for its original instruction hashes.
