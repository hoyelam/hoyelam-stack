# hoyelam-stack

`hoyelam-stack` is a Codex-first engineering workflow that remains portable to other coding agents. It turns a request into a root-cause investigation, architecture-aware implementation, mandatory tests, real runtime verification, and a review loop that resolves every verified finding.

The modular structure is inspired by [pstack](https://github.com/cursor/plugins/tree/main/pstack), adapted into product-neutral instructions with dedicated Codex packaging.

## What it includes

1. `hoyelam-mode` routes non-trivial engineering work through the complete workflow.
2. Specialist agents reconstruct context, investigate root causes, audit comments, review code, design verification, and verify Apple and Electron runtime behavior.
3. Focused skills cover implementation plus context recall, safe checkpoints, reusable real-app verification, Apple-platform verification, Electron DevTools verification, and evidence-gated workflow reflection.
4. Dormant automation packs run a full quality pass, watch a pull request, or propose workflow improvements when explicitly configured.
5. A local validator and GitHub Actions workflow verify the repository itself.

## Start here

1. Read [the workflow](docs/workflow.md).
2. Install the repository locally with [the local setup guide](docs/local-install.md).
3. Invoke `$hoyelam-mode` for implementation work.
4. Invoke `$comment-discipline`, `$prove-the-work`, or `$review-and-resolve` directly for a focused pass.
5. Invoke `$recall-context` before resuming older work and `$checkpoint-work` when pausing unfinished work.
6. Invoke `$verify-apple-apps` for iOS or macOS and `$verify-electron-apps` for Electron.
7. Read [the platform verification guide](docs/platform-verification.md) for evidence expectations and agent routing.

## Core rule

Do not confuse throughput with completion. Work is complete only when the cause is understood, the implementation fits the architecture, tests pass, the real behavior is exercised, the diff is reviewed, and verified findings are resolved.

## License

MIT
