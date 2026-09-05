---
name: review-and-resolve
description: Perform an extensive evidence-backed review of a scoped implementation, verify findings, fix every accepted in-scope issue, and rerun affected checks before completion.
---

# Review And Resolve

## Choose the reviewer

Use an independent reviewer for substantial changes, difficult-to-reproduce failures, or material security, privacy, data-loss, money, permissions, concurrency, migration, or release risk when delegation is available and authorized. Give the reviewer the request, acceptance criteria, complete scoped diff and owning context, tested state, and evidence paths. Ask it to find supported issues without supplying the implementer's preferred verdict. Keep the reviewer read-only; the implementation owner validates findings and owns all accepted fixes.

For small low-risk changes, a deliberate self-review is sufficient. If independent review is unavailable, report that boundary and perform the strongest available review; never call self-review independent. An explicitly required independent review remains a gate.

## Review

1. Establish the intended behavior, architecture, and verified baseline before reading the diff.
2. Review the complete scoped diff and enough surrounding code to understand each changed boundary.
3. Check correctness, root-cause coverage, simplicity, naming, data modeling, architecture fit, concurrency, lifecycle, cancellation, error handling, security, privacy, performance, accessibility, localization, test quality, and user experience where relevant.
4. Look for duplicated state, hidden coupling, unnecessary wrappers, compatibility layers, speculative abstractions, dead paths, and changes that could be smaller.
5. Check tests for meaningful behavior, negative cases, determinism, false confidence, and missing regression coverage. Confirm each acceptance criterion has direct evidence on the final changed state; challenge zero-test passes, unexpected skips, weakened assertions, stale artifacts, and unsupported CI claims using [prove-the-work](../prove-the-work/SKILL.md).
6. Run `$comment-discipline` for comment-specific findings.
7. Verify each candidate finding against code, documentation, a targeted test, or runtime evidence. Drop speculative findings.

## Resolve

1. When implementation is authorized, automatically fix every verified in-scope finding without asking again for routine reversible edits. Simpler designs qualify only when evidence supports a concrete improvement while preserving the requested behavior. A read-only review reports findings without edits.
2. Keep fixes within the task boundary. Report material out-of-scope work separately.
3. Add or adjust tests for behavior changed by review fixes.

## Re-verify

1. After fixes, rerun affected selected checks, builds, and runtime paths against the final state, then inspect the revised diff and touched comments.
2. Repeat review and resolution when new verified in-scope findings remain. Retain current evidence for unaffected claims; if review made no changes, do not rerun checks merely to mark this step done.
3. Ground reviewer disagreements in a reproduction, source contract, or direct observation. Do not churn code to satisfy speculative feedback or loop on unchanged evidence. If a verified issue cannot be resolved within scope or available authority, report it as a blocker without claiming completion.

## Report

Report verified findings, rejected candidates with reason when useful, fixes applied, tests added or changed, exact verification results, remaining out-of-scope work, and worktree state.
