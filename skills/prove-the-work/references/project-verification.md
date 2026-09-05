# Project verification contract

Read this when establishing verification for a project or repairing missing, contradictory, or stale verification guidance. Apply it to any project type; it does not require a new framework or a real-app harness for every repository.

## Establish one supported path

Find the current contract in `AGENTS.md`, contributor documentation, package scripts, build targets, and CI. Reuse that location and tooling. If implementation is authorized and a missing contract prevents reliable proof, document the smallest supported path in the owning project and link it from its agent instructions. During read-only work, report the gap instead. Do not modify other projects merely because the stack is available to them.

Record:

1. Supported working directory, toolchain, dependencies, fixtures, and environment prerequisites without secret values.
2. Exact focused commands and the canonical command for the relevant suite, static checks, and build. Define successful execution, expected test discovery, and legitimate skips.
3. Observable acceptance criteria for the changed behavior and the appropriate runtime or output inspection path.
4. Isolation, evidence capture, and cleanup for checks that mutate state. Prefer disposable fixtures and stop only owned processes.
5. Which checks are required locally and in CI, with platform-specific commands when they differ. Required CI remains pending until it actually runs against the relevant revision.
6. Known coverage gaps, their concrete impact, and how to unblock them. A documented gap is not a waiver or a passing result.

For recurring checks, prefer one existing script or build target shared by local work and CI. It must propagate failures and detect missing expected tests or outputs. Add a wrapper only when it removes repeated ambiguity. When changes to the verification path are in scope, exercise both a valid run and a controlled failure in an isolated fixture; prove that failure reaches the caller. Never deliberately corrupt production state to test the gate.

## Select evidence by surface

| Changed surface | Useful proof |
| --- | --- |
| Library or domain logic | Focused observable behavior tests, boundary/error cases, and affected consumer integration or compatibility checks. |
| Service or API | Request through the supported boundary, response assertions, persisted effects, and applicable authorization/error behavior using isolated state. |
| CLI, automation, or build tooling | Real invocation with disposable inputs; inspect output, exit status, files, and failure propagation. |
| Web, mobile, desktop, or other interactive app | Relevant automated tests plus the changed user path on a fresh artifact; inspect visible state and independent side effects. Use available platform skills. |
| Data, schema, or migration | Representative fixtures, invariants and reconciliation, and applicable retry/recovery checks in an isolated environment. |
| Documentation, prompts, or skills | Check references and examples against their owning source; for behavioral workflow changes, exercise representative requests and failure scenarios. Structural validation alone cannot prove agent behavior. |
| Configuration or CI | Parse and validate the owning format, then exercise the affected command or consuming tool and its failure path when practical. |

Select relevant rows together for mixed projects. Increase depth for security, privacy, money, destructive state, permissions, signing, concurrency, migrations, and releases. Do not add tests that merely repeat wording or implementation. For repeated real-app verification that lacks a reliable control path, use `$build-verification-harness`; for drift in an existing harness, use `$maintain-verification-harness`.

## Maintain with the behavior

Update affected commands, fixtures, acceptance criteria, and mapped features in the same authorized change that alters their contract. Keep intended product behavior authoritative: repair a stale harness without redefining a product regression as success. Rerun changed verification paths and preserve evidence for the final artifact.

Report the requirement, tested state, checks and observed outcomes, remaining gaps, and blockers. A compact task report is enough for routine work; use the project's existing durable evidence format for handoffs and orchestration.
