# Installation and updates

## Install the released plugin in Codex

1. Add the repository marketplace with `codex plugin marketplace add hoyelam/hoyelam-stack --ref main`.
2. Restart Codex so the marketplace refreshes.
3. Install `hoyelam-stack` from the Plugins Directory, or run `codex plugin add hoyelam-stack@hoyelam`.
4. Start a new Codex task so plugin and skill discovery refreshes.

The marketplace resolves the plugin from its tagged GitHub release. It does not require access to a private repository.

## Update the released plugin

1. Refresh the repository marketplace with `codex plugin marketplace upgrade hoyelam`.
2. Reinstall the current release with `codex plugin add hoyelam-stack@hoyelam`.
3. Start a new Codex task.

## Install from source for development

1. Clone the repository with `git clone https://github.com/hoyelam/hoyelam-stack.git`.
2. From the repository root, run `./scripts/install-local.sh`.
3. The script links every `skills/*` directory into `${CODEX_HOME:-$HOME/.codex}/skills`.
4. Run `./scripts/validate.sh` to confirm the source repository.
5. Start a new Codex task so skill discovery refreshes.

Pulling the repository updates linked skills immediately. Check out a tag such as `v0.5.0` when you want a fixed version instead of the latest `main` branch.

## Use with other coding agents

1. Point the agent at the repository `AGENTS.md` for the working agreement.
2. Install or link `skills/` through the agent's supported Agent Skills discovery path.
3. Use `plugin.json` when the runtime supports the open Agent Plugins format.
4. Translate files in `agents/` only when the runtime uses a product-specific custom-agent schema.

## Safety

1. The installer never deletes or overwrites an existing path.
2. An existing symlink to this repository is accepted.
3. Any conflicting file, directory, or symlink stops installation and prints the exact path.
