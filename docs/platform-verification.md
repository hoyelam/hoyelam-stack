# Platform verification

Consult the relevant skill when platform-specific knowledge helps choose or execute proof. Reuse an existing equivalent project command or harness when it already demonstrates the requested behavior.

| Surface | Owning guidance |
| --- | --- |
| iOS tests, builds, and Simulator behavior | [verify-ios-apps](../skills/verify-ios-apps/SKILL.md) |
| macOS applications, builds, and native behavior | [verify-macos-apps](../skills/verify-macos-apps/SKILL.md) |
| Electron main, preload, renderer, and native behavior | [verify-electron-apps](../skills/verify-electron-apps/SKILL.md) |
| Existing Apple invocations or mixed Apple work | [verify-apple-apps](../skills/verify-apple-apps/SKILL.md) |

The Apple entrypoints share their verification contract, references, and readiness helper. The Apple doctor and Electron CDP doctor are optional diagnostics unless the project or user requires them. The owning skills describe tool choices, artifact identity, isolation, and evidence; this guide adds no separate platform checklist.

## Agents and harnesses

The focused skills are discoverable in Codex. `agents/apple-runtime-verifier.md` and `agents/electron-runtime-verifier.md` are portable role briefs, not separately registered Codex agent names. Pass the relevant guidance with scoped verification assignments when it adds needed context.

[Build verification harness](../skills/build-verification-harness/SKILL.md) extends a missing control path while preserving existing project conventions. [Maintain verification harness](../skills/maintain-verification-harness/SKILL.md) handles scoped repair or a full audit. Their owning instructions define coverage and acceptance; successful scoped work does not imply complete application coverage.
