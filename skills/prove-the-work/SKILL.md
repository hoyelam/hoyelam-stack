---
name: prove-the-work
description: Define and execute verification for implementation, documentation, configuration, and tooling changes, with evidence tied to the final state and explicit completion gates.
---

# Prove The Work

Use this method for every change. Scale the checks to the behavior and risk; a prose edit may need only source comparison and link checks. When onboarding a project or repairing missing verification guidance, read the [project verification contract](references/project-verification.md).

## Define success

Before implementation, define observable acceptance criteria and realistic failure modes. These describe what must be true; use the separate planning step below to decide how to prove it.

## Plan verification

1. Inventory the repository's existing tests, static checks, build paths, runtime harnesses, feature maps, observability, available skills, and environment limits.
2. Map each acceptance criterion to an exact command or interaction, the artifact and environment under test, fixtures or prerequisites, expected observable result, and evidence to capture. Choose checks that can disprove the claim, including relevant failure cases and adjacent behavior.
3. Distinguish required checks from optional evidence using the request, repository instructions, CI, and change risk. Route applicable iOS behavior through `$verify-ios-apps` and macOS behavior through `$verify-macos-apps` and applicable Electron behavior through `$verify-electron-apps`.
4. Check tool and control-path availability and run a focused baseline when practical. Name missing coverage, verification setup, and blockers before dependent implementation. Continue independent authorized work when a required check is blocked; keep the verification gap visible.
5. State this plan before implementation and update it when scope or evidence changes. One sentence is enough for a small change; use existing project records for complex or delegated work. Proceed without a new approval unless a missing decision or action requires new authority.
6. For larger changes, identify small verifiable units and the check that closes each one before dependent work proceeds. Include final integration checks; passing isolated units does not prove their composition.

## Execute verification

1. Add or adjust the planned coverage. Prefer focused unit tests for changed behavioral code when the owning boundary can be exercised meaningfully.
2. For a bug, make the test fail for the original reason when a cheap deterministic path exists; record when reproduction is unavailable. Re-run the original reproduction through the same relevant interface after the fix. Cover realistic failure cases and affected adjacent behavior, using assertions on observable outcomes rather than duplicating implementation logic.
3. Use snapshot tests only when pixels, layout, formatting, or rendered structure are the contract.
4. Run the planned focused tests, broader suites, linters, static checks, builds, and packaging. Adapt the plan when new evidence exposes material integration or release risk, keeping acceptance criteria authoritative.
5. Rebuild and restart the real artifact when stale binaries or cached state could hide the result.
6. Exercise the user path with the project-local verification skill, computer use, or a deterministic script when the behavior has a meaningful runtime surface and the environment supports it. Identify mapped features and repeat timing-sensitive or crash-prone paths enough to challenge the original failure.
7. Inspect direct evidence such as UI state, process liveness, logs, persisted values, network results, generated artifacts, crash reports, or traces when relevant.
8. Add a nearby blast-radius check when adjacent behavior is plausibly affected, and prove the key safety fact as far as practical.
9. Rerun selected verification affected by review fixes.

## Evidence standard

For each acceptance criterion and required check, retain the command or interaction, expected and observed result, exit status and test counts when applicable, tested revision or artifact, and relevant logs or artifact paths. Identify uncommitted changes as part of the tested state; a commit hash alone cannot identify a dirty worktree. Keep ordinary evidence in the task report; use existing project records for durable or delegated work.

Use `passed`, `failed`, `blocked`, or `not run` for check results. A pass requires the intended checks to have actually executed and matched the expected result. Zero discovered tests, unexpected skips, a started command, a green exit without expected output, and a reviewer assertion do not prove the behavior.

After any code, fixture, dependency, configuration, generated artifact, or review change, rerun affected checks on the final state. Earlier evidence may be retained only for demonstrably unaffected claims. Rebuild or restart when the running artifact could be stale. CI evidence must match the relevant revision; a local pass does not imply CI passed.

Diagnose failures before retrying. Do not delete or weaken assertions, widen tolerances, skip checks, or change expected behavior merely to obtain a pass. Preserve flaky attempts and report the unresolved failure unless its cause is fixed or evidence establishes an unrelated baseline issue. An unrelated baseline failure remains visible and cannot be reported as a passing required check.

Compilation proves syntax and linkage. Unit tests prove modeled behavior. Runtime checks prove only the paths actually exercised. Required verification that fails or is blocked leaves the task unverified; finish independent authorized work and report the exact blocker and next action. Do not silently downgrade required checks or claim completion. Optional layers may be omitted with a concrete reason and remaining risk. Never rename proxy evidence as a stronger pass.
