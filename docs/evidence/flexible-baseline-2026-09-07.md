# Flexible baseline verification — 2026-09-07

The revised stack retains active lead orchestration and final-state verification while letting agents choose useful skills, tools, and execution order. Package checks, independent review, isolated Codex tasks, observed native delegation, pause/resume, and a real GitHub cache round trip passed the checks described below. Two deliberately unavailable acceptance gates remained correctly blocked.

The original instruction snapshot is commit `9558611deb527380bb28f064b0bfacd4f42956b7`. The revised state is identified by SHA-256 file hashes in the [machine-readable record](flexible-baseline-2026-09-07.json). Earlier evidence records describe their own historical states and were not rewritten. Raw task artifacts are under `.work/stack-simplification/`; that ignored directory and disposable workspaces may expire.

## Changes and acceptance

Personal defaults now live in a shorter `hoyelam-mode`. Skills and references are capabilities to select when useful. Substantial independent work still calls for active delegation, explicit ownership, returned evidence, and lead-owned integration. The task classifier, arbitrary child-count ceiling, mandatory skill chains, and comment-prefix template were removed. Codex guidance favors focused briefs, selective history, artifact references, and worker reuse; actual runtime capacity governs concurrency.

Continuity skills share a compact handoff record. Harness maintenance defaults to the affected scope, with broader audits justified by the request or evidence. Platform and orchestration mechanics remain in their owning skills. Optional source caching and condition-based observation guidance support investigation. Reflection now includes removing redundant rules and observing user interventions and resource use. Role and automation wrappers reference these capabilities without recreating the workflow.

Acceptance was planned before implementation: preserve scope and authorization, demonstrate real behavior and regression detection, keep blocked checks visible, exercise same-repository delegation, verify package discovery, and measure source reduction without equating it with performance. Independent agents owned skill, runtime/harness, and source-cache work; the lead integrated and checked the result.

## Structural and helper verification

| Check | Observed result |
| --- | --- |
| `./scripts/validate.sh` | 74 tests passed, zero skips; 16 skills, 10 agent definitions, and 3 automation packs validated |
| Skill creator `quick_validate.py` on all skill entrypoints | All 16 passed using task-local `uv`/PyYAML after dependency preparation |
| `git diff --check` | Passed |
| Reference-cache tests | 21 tests covering revision reuse/refresh, dirty snapshot preservation, URL/ref rejection, corruption, concurrency, and timeout handling |
| Workflow-exercise helper tests | 11 tests including regression replay, zero-test rejection, scope preservation, post-check mutation detection, and independent CLI inputs |
| Markdown reference checks | Local inline link targets and heading fragments checked, including a broken-fragment regression |

The Markdown checker supports this repository's inline links and ATX headings; it is not a complete Markdown renderer. Reference caching adds no runtime dependency beyond Python, Git, and GitHub CLI for GitHub clones.

Independent review found and resolved an unconditional Electron skill invocation left in platform navigation and three acceptance-checker weaknesses: zero discovered tests could pass, a harness could mutate product files during checking, and module integration could hardcode the visible example. The final checker rejects all three. The complete repository suite was run after those fixes.

## Isolated Codex comparison

Codex CLI `0.153.4` ran ten ephemeral sessions against ordinary disposable projects: five with the archived original skills and five with the revised skills. The configured model was inherited without an override. Project-local `.agents/skills` entries supplied the relevant variant. Candidate prompts described the work without scoring hints; external manifests and acceptance checks remained outside the candidate project.

Projects were created and checked with the shipped helper:

```bash
python3 scripts/workflow_exercises.py prepare --case CASE --stack STACK --dest NEW_PROJECT
codex exec --ephemeral --approve-for-me --skip-git-repo-check --json --color never -C NEW_PROJECT -o RESULT PROMPT
python3 scripts/workflow_exercises.py check --case CASE --project NEW_PROJECT
```

Exact resolved commands, instruction hashes, usage, changed-file summaries, and results are in the machine-readable record. Raw commands, events, outputs, and checks are under `.work/stack-simplification/runs/{a,b}-CASE/`, where `a` is original and `b` is revised. Initial launches combined incompatible `--sandbox` and `--approve-for-me` flags and exited before agent startup. Their errors were retained separately; corrected runs used `--approve-for-me`, which already selects workspace-write. No safeguards were disabled.

| Case | Original | Revised | Observed acceptance |
| --- | --- | --- | --- |
| README CLI example | 24.22 s; 3 tests | 25.67 s; 3 tests | Only README changed; corrected executable example passed |
| Whitespace parser fix | 39.60 s; 7 tests | 38.01 s; 5 tests | Final tests and CLI passed; candidate regression tests failed against the original bug |
| Parser with missing owner acceptance script | 44.49 s; 6 tests | 29.06 s; 6 tests | Implementation passed; both agents explicitly reported final acceptance blocked |
| Pricing, inventory, and composed CLI | 103.75 s; 25 tests | 75.62 s; 13 tests | Domain checks, multiple CLI inputs, invalid input handling, and ownership scope passed |
| Stale verification-harness command | 45.72 s; 3 tests | 48.11 s; 3 tests | Only the harness command map changed; product remained unchanged and unrelated publishing was excluded |

All ten agent processes exited successfully without timing out. External artifact acceptance passed for eight cases. The two intentional blocked cases returned checker status `blocked`, with implementation success and the original missing requirement preserved. The parent separately confirmed that the required `acceptance_check.py` was absent and its command still exited 2. Neither agent invented a substitute or claimed full completion. Independent transcript/result review found no remaining supported outcome, scope, or reporting issue.

These comparisons do not prove delegation. CLI JSON omits native spawn/return events: the original module run announced workers, while the revised run reported delegation unavailable and proceeded directly. Their capability claims cannot be fully verified from those logs. The separate exercise below provides observable delegation evidence.

## Observable orchestration and continuity

In a separate revised-stack module project, native collaboration calls and agent status showed two simultaneous workers. One owned pricing and its tests; the other owned inventory and its tests. The lead owned the composed CLI, inspected returns, integrated the modules, and reused workers for independent review. The parent independently checked the final workspace: **39 tests passed, zero skips**, domain and multiple CLI checks passed, and changes stayed within the assigned files. The example returned `{"total_cents":725,"fulfilled":[2,1,1],"remaining":{"pen":0,"book":0}}`.

Automatic approval review initially rejected the lead's temporary-fixture patch because it did not see the original user authorization and treated fixture instructions as insufficient authority. The root supplied that authorization, the repository's workflow-exercise requirement, and exact writable fixture scope. The same patch and tool were then accepted without bypass. This disclosed the evaluation purpose, so the latter portion of this native exercise was not blinded. Before integration, 27 domain/smoke tests passed while the CLI remained unfinished; the lead correctly withheld completion. Setup and final acceptance are recorded in `.work/stack-simplification/native-setup.json` and `native-check.json`.

Two further fresh Codex sessions exercised checkpoint and recall against a parser workspace. The pause session preserved implementation/test fingerprints and recorded the unfinished state: four tests discovered with one expected failure. The resume session used the handoff, fixed the parser, passed seven tests and six JSON/text CLI cases, and updated the handoff. External checks also replayed its regression tests against the original bug and confirmed failure. Artifacts are under `.work/stack-simplification/continuity/`. This proves the tested pause/resume path, not recovery from every interruption mode.

## Discovery and real source-cache integration

A fresh read-only Codex session discovered `hoyelam-stack:hoyelam-mode` with the revised description, `Personal agent defaults: focused changes, active orchestration, and verified outcomes.`, before its first tool call. Its sole file read returned the full skill body from the installed discovery path. Evidence is in `.work/stack-simplification/discovery.md` and `discovery.events.jsonl`.

After the required `gh auth status --hostname github.com` and `gh api user --jq .login` checks succeeded with the sandbox permissions needed for credential/network access, the source helper cloned the public `hoyelam/hoyelam-stack` repository through GitHub CLI. The request pinned `9558611deb527380bb28f064b0bfacd4f42956b7` and used a task-local cache. Initial creation, reuse, and explicit refresh all returned that revision and the same detached snapshot; the cached main skill matched the archived baseline byte for byte. JSON receipts are retained in the machine-readable record and `.work/stack-simplification/remote-{created,reused,refreshed}.json`.

## Context observations and limits

| Source surface | Original words | Revised words | Reduction |
| --- | --- | --- | --- |
| Main skill | 732 | 427 | 41.7% |
| All 16 skill entrypoints | 6,888 | 5,112 | 25.8% |
| Ten portable role briefs | 1,694 | 580 | 65.8% |
| AGENTS, README, and workflow orientation | 2,362 | 898 | 62.0% |

These are source word counts, not tokenizer counts or measured peak context. Skills are loaded selectively; the combined count does not imply every request loads all entrypoints. Codex reported a skill-description budget warning in all five original runs and one revised run, so reducing this stack did not eliminate pressure from the full installed catalog.

Each comparison has only one synthetic run per variant. Test breadth, cache state, service latency, and runtime differed; the original harness receipt used Python 3.9.10 and the revised harness used Python 3.14. Session-reported usage has unspecified child coverage and cannot establish total multiagent cost. Existing user configuration and the wider skill catalog remained present. Non-Git fixture status checks and one initial parser command failed harmlessly before recovery. The original module run inherited a managed Herdr environment, rejected a parent-pane mismatch after a read-only probe, and performed no observed unrelated writes.

The evidence supports the tested outcomes and shorter instruction surfaces. It does not establish a universal speedup, maximum reliable context size, or optimal concurrency. Unchanged Apple, Electron, and managed Herdr runtime behavior was not revalidated by these general workflow exercises.
