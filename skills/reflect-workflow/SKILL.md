---
name: reflect-workflow
description: Improve reusable agent guidance after user corrections, recurring friction, or a costly failure provides evidence for a change.
---

# Reflect Workflow

Use explicit user preferences, a pattern across at least two tasks, or one high-impact failure with a clear prevention mechanism. Skip trivial work, project-specific facts, and behavior already captured correctly. A complex task alone does not justify new rules.

Reconstruct only the evidence needed to identify the friction and its cause. Consider correctness, unnecessary human intervention, elapsed time, context consumed, repeated tool calls, and delegation overhead where records support those conclusions. Distinguish observations from estimates; do not invent resource measurements. Look for avoidable approvals, repeated discovery, oversized handoffs, and context loaded without affecting a decision.

Prefer deleting, shortening, merging, or narrowing redundant guidance before adding instructions. Identify the existing rule each proposal changes and the failure or wasted effort it prevents. Use executable checks when they fit existing tooling, without introducing dependencies merely to enforce a preference. Update an existing skill first; a new skill needs a distinct useful trigger. Keep project details in their owning project, and keep private source, credentials, and conversation transcripts out of portable guidance.

For reflection-only requests, present recommendations without editing. When improvement is authorized, apply evidence-backed changes within scope and validate the changed skills and plugin. Behavioral rule changes also need representative workflow exercises; structural validation alone does not prove better behavior.

Report the useful changes, evidence, and remaining uncertainty. Include rejected proposals or ideas needing more examples only when they help the user decide.
