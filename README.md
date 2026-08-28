# hoyelam-stack

`hoyelam-stack` is a Codex-first collection of preferred engineering workflows that remains portable to other coding agents. It helps an agent inspect the task, repository, risk, and available tooling, then choose the useful parts of a root-cause-first implementation and verification process.

The modular structure is inspired by [pstack](https://github.com/cursor/plugins/tree/main/pstack), adapted into product-neutral instructions with dedicated Codex packaging.

## What it includes

1. `hoyelam-mode` selects a proportionate workflow for non-trivial engineering work without requiring every task to execute every phase.
2. Specialist agents reconstruct context, investigate root causes, audit comments, review code, design verification, and verify Apple and Electron runtime behavior.
3. Focused skills provide optional depth for implementation, durable multi-unit orchestration, context recall, safe checkpoints, reusable real-app verification, Apple-platform verification, Electron DevTools verification, and evidence-gated workflow reflection.
4. Dormant automation packs run a full quality pass, watch a pull request, or propose workflow improvements when explicitly configured.
5. A local validator and GitHub Actions workflow verify the repository itself.
6. A repository marketplace and tagged releases provide versioned installation and updates.

## Start here

1. Read [the workflow](docs/workflow.md).
2. Install the plugin or its development symlinks with [the installation guide](docs/local-install.md).
3. Invoke `$hoyelam-mode` for implementation work.
4. Invoke `$comment-discipline`, `$prove-the-work`, or `$review-and-resolve` directly for a focused pass.
5. Invoke `$recall-context` before resuming older work and `$checkpoint-work` when pausing unfinished work.
6. Invoke `$verify-apple-apps` for iOS or macOS and `$verify-electron-apps` for Electron.
7. Read [the platform verification guide](docs/platform-verification.md) for evidence expectations and agent routing.
8. Read [the release process](docs/releases.md) and [the changelog](CHANGELOG.md) for versioning details.
9. Invoke `$orchestrate-project` only for programs that span independent units or task contexts.

## Core rule

Use the smallest workflow that produces enough evidence for the task's risk. Completion means every claim is supported, material gaps are named, and verified in-scope findings are resolved; it does not mean every available step ran.

## License

MIT
