---
name: review-and-resolve
description: Review a scoped implementation for supported issues and resolve verified findings when implementation is authorized.
---

# Review And Resolve

## Choose the reviewer

For substantial or risky changes, delegate an independent read-only review when available and authorized. Give the reviewer the request, acceptance criteria, complete scoped diff, relevant owning context, tested state, and evidence. Ask for supported findings without supplying the implementer's preferred verdict. The lead validates findings and owns fixes and integration, directly or through scoped delegation.

For small low-risk changes, a deliberate self-review is sufficient. If independent review is unavailable, report that boundary and perform the strongest available review; never call self-review independent. An explicitly required independent review remains a gate.

## Review

Review the complete scoped diff and enough surrounding context to understand the changed boundaries. Prioritize correctness, the original failure or requested behavior, architecture fit, unnecessary complexity, and the risks actually present. Inspect touched comments and directives; `$comment-discipline` is available for a deeper comment audit.

Challenge whether tests and other evidence prove the requested outcome on the final state. Watch for missing regression coverage, zero-test passes, unexpected skips, weakened assertions, stale artifacts, and unsupported CI claims. Consult [prove-the-work](../prove-the-work/SKILL.md) when evidence is ambiguous.

Verify candidate findings against source contracts, tests, or direct observations. Drop speculative findings and style preferences without a concrete benefit.

## Resolve

When implementation is authorized, fix verified in-scope findings without asking again for routine reversible edits. Simpler designs qualify when evidence supports a concrete improvement while preserving requested behavior. A read-only review reports findings without edits. Report material out-of-scope work separately.

After fixes, rerun affected checks against the final state and inspect the revised diff. Add or adjust coverage when changed behavior needs it. Retain current evidence for unaffected claims; if review made no changes, do not rerun checks merely to mark this step done.

Repeat review when new verified issues remain, using evidence to resolve disagreements. Do not churn code for speculative feedback or loop on unchanged evidence. An unresolved verified in-scope issue or failed or blocked required check prevents a completion claim; continue independent authorized work and report the blocker.

## Report

Lead with supported findings or the resolved outcome, then the evidence and remaining limits. Include rejected candidates only when the reason matters to the decision.
