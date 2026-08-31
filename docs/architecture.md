# Repository architecture

## Portable core

1. `AGENTS.md` carries the repository-wide working agreement.
2. `skills/` contains product-neutral Agent Skills.
3. `agents/` contains specialist-agent definitions that compatible runtimes can adopt or translate.
4. `plugin.json` exposes the portable skill package through the open Agent Plugins format.
5. `.codex-plugin/plugin.json` adds Codex-specific presentation and discovery metadata.

Apple and Electron runtime verification each have a platform skill, supporting references and doctor script, and a dedicated read-only verifier agent. The generic runtime verifier routes to them.

## Local layer

1. `scripts/install-local.sh` installs idempotent symlinks.
2. Codex receives each skill through its local skill directory.
3. Other coding agents can consume `AGENTS.md`, the open plugin manifest, or the skill directories through their supported discovery mechanism.
4. The source repository remains authoritative; edits appear locally without copying files.

## Verification infrastructure layer

1. `build-verification-harness` creates a project-local control skill, executable helpers, and an indexed feature map when repeated runtime proof would otherwise be improvised.
2. `maintain-verification-harness` reconciles that control surface with current source and exercises every mapped feature without changing product behavior.
3. Apple and Electron platform skills define platform safety and evidence contracts; project-local harnesses compose them with application-specific launch, interaction, fixtures, and proof paths.
4. Structured orchestration receipts bind runtime evidence to the application revision, harness revision, doctor result, mapped features, and preserved artifacts.

## Orchestration layer

1. `orchestrate-project` coordinates programs that span independently executable units or task contexts.
2. Its dependency-free runtime stores project-local program state, units, worker assignments, numbered attempts, thread identities, exclusive scope leases, inbox events, gates, verification receipts, standing orders, and generated status under `.hoyelam/orchestrate/`.
3. File locking, atomic writes, orphan cleanup, and full-store preflight protect concurrent and interrupted state updates; exact opaque lease conflicts and hierarchical `repo:` path conflicts prevent two active units from claiming the same canonical mutable scope.
4. Verification is keyed to the current unit revision, so an artifact change invalidates older evidence.
5. Ordinary tasks do not pay the orchestration cost.

## Delegation layer

1. `hoyelam-mode` owns direct-task routing and keeps repository metadata discovery, decisions, integration, and final reporting in the parent.
2. A small deterministic router encodes the default `0–3` child policy for representative task shapes.
3. Codex-specific fork, capacity, reuse, control, and report guidance lives in a conditional reference so the portable core does not prescribe unavailable tools to other agents.

## Automation layer

1. `automations/full-quality-pass` finishes a completed implementation through verification and review.
2. `automations/pr-quality-watch` watches a configured pull request and keeps it review-ready.
3. `automations/workflow-reflection` analyzes configured completed work and proposes evidence-backed improvements.
4. All packs are dormant source material until the user explicitly creates an automation.
5. No automation merges, deploys, or widens the requested scope.

## Validation layer

1. `scripts/validate.py` validates manifests, skill frontmatter, agent frontmatter, automation files, and placeholders.
2. `tests/` covers the validator, local installer, platform verification scripts, and orchestration runtime.
3. `.github/workflows/validate.yml` runs the same local command in repository CI.
