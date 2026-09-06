# Repository architecture

## Portable core

1. `AGENTS.md` carries the repository-wide working agreement.
2. `skills/` contains product-neutral Agent Skills.
3. `agents/` contains specialist-agent definitions that compatible runtimes can adopt or translate.
4. `plugin.json` exposes the portable skill package through the open Agent Plugins format.
5. `.codex-plugin/plugin.json` adds Codex-specific presentation and discovery metadata.

iOS, macOS, and Electron have dedicated verification entrypoints. iOS and macOS share Apple references, diagnostics, and a read-only verifier agent. The existing Apple skill remains a shared route. These tools supplement supported project harnesses; the generic runtime verifier routes to the relevant platform.

## Local layer

1. `scripts/install-local.sh` installs idempotent symlinks.
2. Codex receives each skill through its local skill directory.
3. Other coding agents can consume `AGENTS.md`, the open plugin manifest, or the skill directories through their supported discovery mechanism.
4. The source repository remains authoritative; edits appear locally without copying files.

## Verification infrastructure layer

1. `build-verification-harness` creates or extends a repeatable project verification path, with an optional control-skill and feature-map template when repeated runtime proof would otherwise be improvised.
2. `maintain-verification-harness` reconciles that control surface with current source and exercises every mapped feature without changing product behavior.
3. Apple and Electron platform skills define platform safety and evidence contracts; project-local harnesses compose them with application-specific launch, interaction, fixtures, and proof paths.
4. Orchestration evidence identifies the application artifact, harness when relevant, exercised behavior, and preserved results. The bundled harness schema also records doctor status and mapped features; existing formats can carry equivalent evidence.

## Orchestration layer

1. `orchestrate-project` coordinates programs that span independently executable units or task contexts.
2. Existing project records can satisfy the playbook’s ownership, dependency, recovery, and evidence requirements. Its optional dependency-free runtime stores project-local program state, units, worker assignments, numbered attempts, thread identities, exclusive scope leases, inbox events, gates, verification receipts, standing orders, and generated status under `.hoyelam/orchestrate/`.
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

1. `scripts/validate.py` validates manifests, skill frontmatter, agent frontmatter, automation files, local Markdown resource links, and placeholders. File discovery excludes Git metadata and local `.work`, `.hoyelam`, and `__pycache__` state.
2. `tests/` covers the validator, local installer, platform verification scripts, and orchestration runtime.
3. `.github/workflows/validate.yml` runs the same local command to check this plugin repository. It is repository maintenance infrastructure; using the skills does not require GitHub Actions or any CI service.
