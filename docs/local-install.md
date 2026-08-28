# Local installation

## Install for Codex

1. From the repository root, run `./scripts/install-local.sh`.
2. The script links every `skills/*` directory into `${CODEX_HOME:-$HOME/.codex}/skills`.
3. Start a new Codex task so skill discovery refreshes.
4. Run `./scripts/validate.sh` to confirm the source repository.

## Use with other coding agents

1. Point the agent at the repository `AGENTS.md` for the working agreement.
2. Install or link `skills/` through the agent's supported Agent Skills discovery path.
3. Use `plugin.json` when the runtime supports the open Agent Plugins format.
4. Translate files in `agents/` only when the runtime uses a product-specific custom-agent schema.

The `.codex-plugin/plugin.json` manifest is also ready for a marketplace-backed installation after the repository and marketplace destination are chosen.

## Safety

1. The installer never deletes or overwrites an existing path.
2. An existing symlink to this repository is accepted.
3. Any conflicting file, directory, or symlink stops installation and prints the exact path.
