# Repository architecture

## Portable capabilities

[Hoyelam Mode](../skills/hoyelam-mode/SKILL.md) owns personal defaults and the completion standard. `AGENTS.md` adds this repository's verification requirements. The README and usage guide explain discovery without duplicating the working rules.

`skills/` contains independently selectable capabilities. Entrypoints hold the essential guidance; references hold conditional procedures; scripts automate repeated operations. iOS and macOS share Apple references and diagnostics. The focused platform entrypoints remain discoverable alongside Electron verification.

`agents/` contains optional role briefs referencing their owning skills. These are source definitions, not a promise that Codex registers ten callable agent types. Use native subagents with a scoped brief where the runtime does not load custom agents.

## Codex and other runtimes

`.codex-plugin/plugin.json` exposes the skills to Codex. `plugin.json` describes the portable package. `scripts/install-local.sh` links source skills into the local Codex skill directory; installed symlinks follow source changes. Other agents can consume supported skill directories and translate optional role briefs.

[Delegation guidance](../skills/hoyelam-mode/references/single-task-delegation.md) keeps assignment and integration responsibilities portable. Conditional Codex and Herdr references hold host mechanics. Worker count follows useful independent work and runtime capacity, without a model-specific ceiling or task classifier.

## Optional tools

- The [source-research helper](../skills/investigate-first/references/source-research.md) reuses reference repositories and identifies the exact revision inspected.
- [Verification harnesses](../skills/build-verification-harness/SKILL.md) reuse project commands and provide launch, drive, observation, and cleanup knowledge. [Maintenance](../skills/maintain-verification-harness/SKILL.md) distinguishes scoped repairs from full audits.
- [Orchestration](../skills/orchestrate-project/SKILL.md) supports simple task-owned records or the bundled runtime. The runtime adds assignments, attempt identity, exclusive scope leases, inbox events, revision-bound verification, and interruption recovery under `.hoyelam/orchestrate/`. Locking, atomic writes, and preflight checks protect its records. Runtime closure checks bookkeeping; acceptance still needs behavior evidence.
- `automations/` contains dormant source packs for quality review, PR maintenance, and workflow reflection. Scheduling and external actions require configured authority.

## Verification

`./scripts/validate.sh` checks manifests, skills, agent briefs, automation packs, local documentation references, placeholders, and Python tests. Tests exercise installer behavior, reference caching, platform diagnostics, orchestration integrity, and workflow fixture helpers. Local `.work`, `.hoyelam`, Git metadata, and Python caches are excluded from package discovery.

[Workflow exercises](../skills/hoyelam-mode/references/workflow-validation.md) validate actual agent behavior separately. They retain versioned evidence and measure context/effort where available. GitHub Actions runs the package check; using the stack does not depend on a CI provider.
