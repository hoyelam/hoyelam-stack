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

## Automation layer

1. `automations/full-quality-pass` finishes a completed implementation through verification and review.
2. `automations/pr-quality-watch` watches a configured pull request and keeps it review-ready.
3. `automations/workflow-reflection` analyzes configured completed work and proposes evidence-backed improvements.
4. All packs are dormant source material until the user explicitly creates an automation.
5. No automation merges, deploys, or widens the requested scope.

## Validation layer

1. `scripts/validate.py` validates manifests, skill frontmatter, agent frontmatter, automation files, and placeholders.
2. `tests/` unit-tests the validator.
3. `.github/workflows/validate.yml` runs the same local command in repository CI.
