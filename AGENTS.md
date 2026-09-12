# hoyelam-stack working agreement

Use [hoyelam-mode](skills/hoyelam-mode/SKILL.md) for personal defaults and the completion standard.

## Repository verification

Run `./scripts/validate.sh` from the repository root to check package structure, documentation references, and the Python unittest suite. Inspect actual test discovery and skips. The suite uses local disposable fixtures and mocked external services; run it, fix failures caused by the requested change, and rerun affected checks within the task's existing authority.

Behavioral instruction changes also require [isolated workflow exercises](skills/hoyelam-mode/references/workflow-validation.md). Record the instruction version, actual actions, observed outcomes, and limitations. Historical evidence remains tied to the state it tested.

## Ownership

Keep platform procedures in their verification skills and runtime mechanics in their adapters. Prefer existing equivalent project tooling. [Comment discipline](skills/comment-discipline/SKILL.md) owns the preference for clear code and useful, minimal comments; do not duplicate its rules here.
