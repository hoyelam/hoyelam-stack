---
name: review-and-resolve
description: Perform an extensive evidence-backed review of a scoped implementation, verify findings, fix every accepted in-scope issue, and rerun affected checks before completion.
---

# Review And Resolve

## Review

1. Establish the intended behavior, architecture, and verified baseline before reading the diff.
2. Review the complete scoped diff and enough surrounding code to understand each changed boundary.
3. Check correctness, root-cause coverage, simplicity, naming, data modeling, architecture fit, concurrency, lifecycle, cancellation, error handling, security, privacy, performance, accessibility, localization, test quality, and user experience where relevant.
4. Look for duplicated state, hidden coupling, unnecessary wrappers, compatibility layers, speculative abstractions, dead paths, and changes that could be smaller.
5. Check tests for meaningful behavior, negative cases, determinism, false confidence, and missing regression coverage.
6. Run `$comment-discipline` for comment-specific findings.
7. Verify each candidate finding against code, documentation, a targeted test, or runtime evidence. Drop speculative findings.

## Resolve

1. Fix every verified in-scope finding, including simpler or more concise designs that preserve the requested behavior.
2. Keep fixes within the task boundary. Report material out-of-scope work separately.
3. Add or adjust tests for behavior changed by review fixes.
4. Rerun the selected checks, builds, runtime verification, comment audit, and final diff inspection affected by the fixes.
5. Repeat review until no verified in-scope findings remain.

## Report

Report verified findings, rejected candidates with reason when useful, fixes applied, tests added or changed, exact verification results, remaining out-of-scope work, and worktree state.
