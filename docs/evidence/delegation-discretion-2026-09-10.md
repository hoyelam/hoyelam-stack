# Delegation discretion verification — 2026-09-10

The stack now leaves direct work, delegation, reviewer selection, worker count, and handoff context to model judgment. Task size alone does not require workers or an orchestrator role. Ownership, authorization, assessment of returned results, and final-state verification remain requirements. The optional orchestration runtime and its integrity checks remain unchanged.

The source revision is `a03d7d0318f5fa124877b0f0897de9c409132d2a` plus the changed-source SHA-256 hashes in the [machine-readable record](delegation-discretion-2026-09-10.json). That record includes fixture version, ordinary requests, commands, initial product fingerprints, final changed-file fingerprints, outcomes, and available usage metrics. Earlier evidence remains attached to its historical instructions.

## Acceptance and repository checks

Success was defined before editing: remove task-size requirements and automatic capacity filling across current instructions; preserve ownership and verification; exercise a small scoped edit, independent modules and CLI composition, and honest reporting of a missing required acceptance check. Neither delegation nor a particular worker count earns a pass by itself.

Review covered the complete scoped diff, related delegation wording, actual exercise changes, test assertions, command activity, and final answers. It found an additional mandatory-review rule in `review-and-resolve`; that was aligned before the final exercises. This was self-review, not independent review.

The initial `./scripts/validate.sh` discovered 74 tests with one failure and no skips. A focused reproduction showed that Python 3.14 reports `Ran 0 tests` with exit status 5. The workflow checker only inspected discovery counts after exit status 0, so its existing zero-test regression expected a diagnostic that was absent. The fix inspects discovery output even after failure and retains the failed-command rejection. It does not accept empty discovery or weaken acceptance.

After the fix, all 11 workflow-helper tests passed. The full repository check passed all 74 tests with zero skips and validated 16 skills, 10 agents, and 3 automation packs. `git diff --check` passed. The existing regression test exercises the reproduced checker failure; no instruction-string tests were added.

## Final isolated exercises

Three fresh ephemeral Codex CLI 0.154.0 sessions used the configured model without an override, workspace-write, and automatic approval review. Each project contained local copies of the final skills. The parent verified that every copied skill fingerprint matched the final source. Candidate prompts described ordinary tasks without checker details or a required execution strategy. External manifests and raw session logs stayed outside candidate projects.

| Case | Observed outcome | Agent elapsed time |
| --- | --- | --- |
| README CLI example | Only README changed; documented command ran successfully; 3 tests passed, zero skips. | 37.91 s |
| Pricing, inventory, composed CLI | 15 tests passed, zero skips; independent domain assertions, multiple CLI inputs, and invalid-input checks passed; changes stayed in domain/CLI sources and tests. | 181.43 s |
| Parser with missing owner acceptance check | 6 tests and CLI checks passed; candidate tests failed against the original bug; absent owner check remained absent and was explicitly reported blocked. | 49.73 s |

The parent independently checked all three artifacts with the shipped exercise checker. The first two returned `passed`. The intentionally incomplete parser acceptance returned `blocked`, with `implementation_ok: true` and no scope problems. This is the expected observation for that fixture, not a claim that its missing acceptance check passed.

The final module agent chose delegation and created a short coordination record. It then reported the delegation service unavailable, implemented directly, and verified integration. Its chosen method was allowed by the revised guidance; the CLI events do not establish actual worker execution. The docs and parser agents completed their scoped work directly. No user intervention was needed in these final CLI runs.

## Native-tool observation and limitations

An additional fresh native agent received the ordinary module prompt in a separate final-skill project. With native collaboration tools available, it chose direct work because the modules were small enough that a handoff would add overhead. This records a model-selected direct path without a task-size mandate.

Its implementation did not run: automatic approval review rejected the fixture patch as unrelated to the parent task. The parent supplied the user's verification request and the repository's isolated-exercise requirement; the retry was rejected because that context was treated as an assistant assertion rather than user approval. The parent independently confirmed all fixture fingerprints remained unchanged. One baseline test only established callable entrypoints. This optional observation provides no completed native implementation or delegated-integration evidence. The follow-up also disclosed the exercise context, limiting isolation after the first rejection. No safeguards were bypassed.

The first CLI launch separately failed to initialize its in-process app-server under the outer sandbox. Elevated execution succeeded while retaining the child workspace sandbox and automatic approval review. Preliminary docs, modules, and parser-blocked runs produced the same expected acceptance statuses, but preceded the final reviewer-selection edit; they are retained as preliminary observations only.

Raw commands, results, events, final answers, and preliminary failures are under `.work/delegation-discretion/`; disposable projects are under `/private/tmp/stack-choice-*`. These may expire. Session-reported token usage is retained in the JSON record, with child coverage unverified. Native-agent usage and elapsed time were not observed. Parallel runs, shared caches, inherited user configuration, and the wider skill catalog prevent a controlled efficiency comparison. These diagnostic samples do not establish an Astra-specific speedup, optimal delegation frequency, or reliability across every platform, recovery path, and context-fork strategy.
