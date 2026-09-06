# hoyelam-stack working agreement

Use [hoyelam-mode](skills/hoyelam-mode/SKILL.md) as the maintained engineering method: understand, define success, plan verification, implement, verify, review and resolve, re-verify, report evidence. Verification governs completion and orchestration governs substantial independent work. Scale depth to risk and preserve the user's scope and authority.

## Repository verification

Run `./scripts/validate.sh` from the repository root. It checks package structure and documentation references and runs the Python unittest suite. Inspect counts and skips; success requires validation and discovered tests to pass.

Workflow behavior changes also require [isolated workflow exercises](skills/hoyelam-mode/references/workflow-validation.md). Structural validation alone cannot prove agent behavior. Record the instruction version, actual commands and edits, observed outcomes, and limitations. Keep historical evidence tied to the state it tested.

Plan acceptance checks before implementation. After review fixes, rerun affected checks on the final state. Required checks explicitly requested by the user remain required; blocked or failed checks leave verification incomplete. Preserve failure evidence, do not weaken tests to obtain a pass, and retain still-current evidence when no relevant state changed.

Platform verification lives in `verify-ios-apps`, `verify-macos-apps`, and `verify-electron-apps`. Use existing equivalent project tooling when it can prove the same outcome. Keep platform details and optional orchestration runtime mechanics in their owning skills rather than duplicating them here.

## Comments

1. Prefer code, types, names, tests, runtime checks, and tooling over comments.
2. Keep legal and license headers.
3. Keep a comment only for a proven external constraint that cannot be made obvious or executable.
4. Prefix rare constraint comments with exactly one of `IMPORTANT`, `DO NOT REMOVE`, `TOO RISKY`, or `FINE FOR NOW`.
5. Every prefixed comment must name the external constraint, evidence source, failure mode, and removal condition when one exists.
6. Treat the prefix as a review trigger, not proof that the comment deserves to remain.
7. Remove narration, section banners, commented-out code, workaround stories, stale TODOs, and comments that repeat the code.
