# hoyelam-stack

`hoyelam-stack` captures how I like to work with coding agents: focused changes, model-directed delegation, and evidence that the result works. Codex is my preferred agent; the skills remain usable by other coding agents.

I want agents to choose useful methods and tools. A fixed sequence of phases or mandatory skill calls adds little when the agent already knows how to do the work. The [personal defaults](skills/hoyelam-mode/SKILL.md) are the maintained source for my working preferences and completion standard.

## What matters to me

I want the model to decide whether delegation improves speed, quality, or context management. Task size alone does not require workers or an orchestrator role. When delegating, the lead owns clear boundaries, assessment of results, and the integrated outcome. The [orchestration skill](skills/orchestrate-project/SKILL.md) provides more coordination when dependencies, concurrent ownership, or interruptions justify it.

Verification gives me confidence. Tests, real usage, and review provide different evidence; the depth should fit the changed behavior and risk. I expect accurate results, checks against the final state, and clear reporting when required proof is blocked. [Prove the work](skills/prove-the-work/SKILL.md) helps design or assess that evidence.

Context is a working resource. Skills should be independently useful, keep their entrypoints small, and expose details when needed. Workers should receive focused briefs and return concise evidence with artifact paths. [Codex delegation guidance](skills/hoyelam-mode/references/codex-delegation.md) covers context and worker reuse without pinning a model or context-window size.

## Capabilities

The [capability guide](skills/hoyelam-mode/SKILL.md#available-capabilities) helps agents select investigation, verification, review, platform, continuity, and reflection skills. Each can also be invoked directly.

The stack includes iOS, macOS, and Electron verification guidance, optional readiness diagnostics, and skills for building or repairing a project-local verification harness. They reuse supported project tooling. See [platform verification](docs/platform-verification.md).

The source-research helper caches reference repositories at explicit revisions. The orchestration runtime supplies durable assignments, ownership checks, and recovery when those capabilities are useful. These tools support the work without becoming prerequisites for ordinary tasks.

## Use and maintain

Follow the [installation guide](docs/local-install.md), then invoke `$hoyelam-mode` or reference it in project instructions. Installing the stack makes capabilities available; the agent loads their bodies as needed. The [usage guide](docs/workflow.md) gives examples.

Run `./scripts/validate.sh` to validate the package and helper tests. Behavioral changes also use [isolated workflow exercises](skills/hoyelam-mode/references/workflow-validation.md), comparing actual outcomes and costs when evaluating efficiency. See [architecture](docs/architecture.md), [design evidence](docs/design-evidence.md), [releases](docs/releases.md), and the [changelog](CHANGELOG.md).

## License

MIT
