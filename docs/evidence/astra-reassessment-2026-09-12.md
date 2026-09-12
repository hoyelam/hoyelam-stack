# Astra-first stack reassessment — 2026-09-12

The user authorized implementing the recommendations from the stack audit against [OpenAI's Astra skills and prompting article](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), including verification on Astra and Sol. Implementation, local validation, and the requested comparative exercises are complete. All 14 artifact checks produced the expected functional status; bounded workflow deviations and limitations are recorded below.

## Implemented scope

- Keep one shared engineering core. Clarify persistence through the requested working result, verification, and supported in-scope repairs while preserving read-only review and authorization boundaries.
- Front-load all 16 skill descriptions with their distinguishing task. Total description text decreased from 1,983 to 1,280 characters, a 35.5% reduction; this is a source measurement, not a performance result.
- Align hoyelam-mode, review-and-resolve, prove-the-work, and comment-discipline invocation metadata with their bodies.
- Select architecture sources by the decision being made. Apple and Electron verification consult general proof guidance only when acceptance or evidence is unclear. Platform procedures, artifact identity, profile isolation, cleanup ownership, and required checks remain intact.
- Make the Apple compatibility router explicit-only while retaining the focused iOS and macOS entrypoints.
- Simplify repository instructions and document reversible discovery choices and model comparison settings.

Machine-local changes simplify the user-level AGENTS.md to reference the maintained core and preserve its GitHub section byte-for-byte. Three existing local alternatives gained explicit-only metadata: karpathy-guidelines, public/swiftui-ui-patterns, and public/swift-concurrency-expert. Their skill bodies were not changed. The retained owners are hoyelam-mode, the build-ios-apps SwiftUI patterns skill, and swift-concurrency respectively. No plugin was uninstalled, cache edited, or global model selection changed. These local choices are not applied by the portable installer.

The original global instructions are backed up under `.work/astra-reassessment/global-before.md`. To undo local selection changes, remove the three newly added agents/openai.yaml files or restore implicit invocation. Third-party updates may replace these metadata overrides. Start a fresh task after changing discovery policy.

## Evidence

The [machine-readable record](astra-reassessment-2026-09-12.json) retains the source revision, before/after instruction hashes, local setting hashes, fixture and runner hashes, check commands, observations, and limitations. Historical evidence was not rewritten.

| Check | Observed result |
| --- | --- |
| `./scripts/validate.sh`, before and after edits | 74 tests passed, zero failures or skips; 16 skills, 10 agents, and 3 automation packs validated. |
| Skill-creator validator and YAML metadata checks | All 19 stack/local skills passed; four explicit-only policies and the unchanged GitHub section confirmed. |
| `git diff --check` | Passed. |
| Independent source review | No supported findings in the repository diff, global instruction diff, or three installed metadata files. |
| Fresh CLI prompt preview | 112 ordinary discovery entries; all four explicit-only skills omitted and selected revised stack descriptions displayed in full. |
| Explicit Apple-router invocation | A fresh Astra task loaded the copied explicit-only router and both platform skills, selected proportional evidence, and made no changes or product-check invocations. |

The CLI catalog differs from the already-running desktop catalog, so 112 cannot be compared directly with this conversation's original skill count. Existing sessions retain their earlier discovery context. Some model exercises still emitted description-budget warnings alongside the installed catalog and copied project skills; this pass does not eliminate every catalog-budget issue. The Apple router received a live explicit-invocation check. The three installed third-party alternatives received metadata and discovery checks, without sending their bodies to a model. [OpenAI documents the explicit-only policy](https://learn.chatgpt.com/docs/build-skills).

The stock Python lacked PyYAML. Its temporary installation initially failed under sandbox DNS, then succeeded with approved elevation. The existing validator ran using only the task's temporary dependency cache; no repository dependency was added.

## Comparative workflow observations

The comparison used current and revised frozen skill copies on the same docs, parser-blocked, and modules fixtures with gpt-6-astra and gpt-5.6-sol at medium reasoning, plus the final harness-repair fixture on both models. Requests and independent artifact checkers came from the existing workflow exercise helper. Candidate projects contained synthetic standard-library applications and copied skills; logs and checker manifests stayed outside those projects. All copied skill hashes matched their selected frozen snapshot and remained unchanged. Each matched pair had identical non-skill starting files.

| Model | Task | Baseline seconds | Revised seconds | Functional result |
| --- | --- | --- | --- | --- |
| Astra | README command | 27.76 | 31.50 | Only README changed; documented command and 3 tests passed. |
| Sol | README command | 53.88 | 29.78 | Only README changed; documented command and 3 tests passed. |
| Astra | Parser with missing owner check | 37.66 | 41.60 | 6 tests and CLI checks passed; missing final acceptance correctly reported blocked. |
| Sol | Parser with missing owner check | 51.67 | 43.91 | 4 tests and CLI checks passed; missing final acceptance correctly reported blocked. |
| Astra | Modules and CLI integration | 121.62 | 142.03 | Domain assertions and CLI fixtures passed; baseline 13 tests, revised 16. |
| Sol | Modules and CLI integration | 114.53 | 108.92 | Domain assertions and CLI fixtures passed; baseline 11 tests, revised 9. |

Both final harness tasks repaired only the split command mapping, reproduced the original control failure against a working product command, ran structural validation, live doctor/split/cleanup checks, and passed three required product tests. Product files and account configuration stayed unchanged. Astra completed in 77.60 seconds and Sol in 105.20 seconds. Unavailable account publishing was correctly excluded from the scoped repair.

Independent review inspected actions, source, tests, final responses, and checker assertions for all 14 runs. Every parser regression suite failed when replayed against the original bug. All four parser agents attempted the missing acceptance command, left it absent, and accurately reported the gap. The four intentionally blocked fixture results are expected observations, not failures of this stack's acceptance checks. The module agents worked directly and verified composition; these runs do not establish delegated integration behavior. No unnecessary user approval was requested inside the model tasks.

The evidence also records bounded deviations. Both Sol module test suites used auto-cleaned TemporaryDirectory fixtures outside the project-requested `.work` location. Sol's harness agent listed sibling AGENTS.md paths without reading their contents or evaluation results, read an unrelated publishing feature document, and repeated checks after an evidence-only edit. Non-Git fixtures triggered unnecessary Git commands; some compound command events masked an earlier failure or omitted CLI stdout, so independent checker evidence is necessary. These observations do not justify claiming perfect instruction adherence or a universal efficiency improvement.

Timing and session-reported input/output/cache usage are retained in the JSON record. Results are mixed: the revised Astra samples took longer, while the revised Sol samples took less time. Different generated tests, cache usage, shell batching, shared-machine concurrency, and one sample per case prevent attributing those differences to the instructions. Matched pairs share the final global instructions and CLI configuration while varying project-local skills; they do not compare the old/new global settings or isolate the desktop environment. Native Apple/Electron runtime reliability and all architecture-routing branches remain outside these synthetic Python exercises.

## Execution boundaries and retained failures

An initial CLI flag combination was rejected before execution and corrected. The next launch failed to initialize its local app-server under the outer sandbox. Automatic approval review initially rejected elevated model execution; the user then explicitly approved the OpenAI egress and child edits in disposable workspaces. All subsequent fixture sessions retained workspace-write and automatic approval review. The failed launches remain recorded separately from the comparison.

An optional live invocation check of installed third-party skills was separately rejected for its additional payload. A narrower check using only the already-approved copied Apple router succeeded in 37.80 seconds. It read the explicit-only router, both focused platform skills and their shared contract, without loading prove-the-work, changing files, or launching products. Local metadata/discovery checks cover the three third-party alternatives. No rejected payload was sent and no safeguards were bypassed.
