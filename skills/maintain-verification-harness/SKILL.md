---
name: maintain-verification-harness
description: Repair a project verification skill when its control paths or feature map drift, or audit its coverage when requested.
---

# Maintain Verification Harness

Maintain the bundled verification-skill and feature-map format using its [harness contract](../build-verification-harness/references/harness-contract.md). Keep an equivalent existing harness's conventions and supported maintenance checks; it needs no migration.

## Bound the work

Locate the owning harness and inspect repository instructions, the affected scenarios, recent changes, and their current source paths. Default to a scoped repair: selected control commands, mapped features, and relevant regressions. Perform a full-map audit when requested or when evidence of wider drift prevents bounding the affected surface. State the chosen coverage and required checks before editing.

Edit harness-owned files within the task's authority. Read product source to reconcile behavior, but keep product fixes separate unless authorized. Update expectations for intentional changes; report broken product behavior instead of documenting the regression as expected.

## Reconcile and exercise

- Check feature-index integrity and reconcile selected entries with actual user routes, labels or identifiers, prerequisites, variants, and observable effects. Add missing coverage only when a current source path and user route support it.
- Use the harness's isolation model. Drive shared state serially unless independent instances are supported. Establish readiness and instance identity before driving, and recheck after relaunch or surprising results using the supported doctor or equivalent check.
- Exercise every selected feature through its real user path and every changed control path against the current artifact. Include nearby regressions relevant to the repair; a full audit selects every mapped feature. Record unreachable paths and their exact missing prerequisites.
- Preserve evidence through failures and cleanup. Stop only processes the pass started and remove only its scratch state. Rerun affected paths after fixes.

## Report the coverage

Run `python3 <build-verification-harness-skill>/scripts/validate_harness.py <project-verification-skill>` for the bundled format, plus the selected live checks. Report `clean` when selected coverage passes without corrections, `changed` when repairs pass those checks, or `blocked` when required proof remains unavailable or failing.

Name the scope, features and control paths checked, artifact identity, observations, and material untested boundaries. A successful scoped repair does not establish a clean full map. Include product findings and the next action for blockers separately. Existing task authority governs commits and external actions; this skill grants no additional authority.
