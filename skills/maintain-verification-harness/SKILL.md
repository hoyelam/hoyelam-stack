---
name: maintain-verification-harness
description: Audit and repair an existing project-local verification skill and feature map when application behavior or its control path may have drifted.
---

# Maintain Verification Harness

This skill maintains the bundled verification-skill and feature-map format. For an existing harness with a different structure, use its supported maintenance checks and `$prove-the-work`; do not migrate it just to satisfy this template.

## Locate and bound the pass

1. Find the project-local verification skill that owns launch, doctor, drive, evidence, cleanup, and an indexed feature map. If several are plausible and the requested scope does not identify one, ask which surface is in scope.
2. Read the repository instructions, the target skill, its feature map, and the [project harness contract](../build-verification-harness/references/harness-contract.md).
3. Edit only files owned by the verification skill. Read product source to reconcile behavior, but do not change product behavior during maintenance.
4. Choose one outcome: `clean`, `changed`, or `blocked`.

## Reconcile source and map

1. Check that every indexed feature file exists, every feature file is indexed once, identifiers are stable, and links resolve.
2. For each feature, locate its current source entry points, visible labels or identifiers, variants, prerequisites, and observable effects.
3. Update documentation when the application changed intentionally. Treat working behavior that the harness cannot drive as a harness gap. Report behavior that is actually broken as a product finding instead of describing the regression as expected behavior.
4. Sweep recent user-facing changes for concrete features missing from the map. Add one only when a current source path and user route support it.

## Run the live pass

1. Use the target skill's isolation model. Run one serial instance unless the skill explicitly proves independent instances are safe.
2. Run doctor before the first drive, after a surprising result, and after any relaunch or fresh session.
3. Exercise every mapped feature at least once through a real user path. Record unreachable features with the exact account, permission, entitlement, platform, or external-state prerequisite.
4. Preserve evidence across failed attempts and cleanup. Remove only residue created by the pass and stop only processes the harness started.
5. Re-run every changed harness path against the real artifact before accepting it.

## Finish

1. `clean`: every feature received source and live coverage, and no correction remains.
2. `changed`: all harness or map corrections are within the verification skill, validated, and proven live.
3. `blocked`: name the uncovered features, attempted routes, evidence collected, and exact blocker.
4. Run `python3 <build-verification-harness-skill>/scripts/validate_harness.py <project-verification-skill>` before reporting `clean` or `changed`.
5. Report product findings separately from harness maintenance.
6. Do not commit, publish, open a pull request, schedule recurring work, or contact an external system without the user's authority.
