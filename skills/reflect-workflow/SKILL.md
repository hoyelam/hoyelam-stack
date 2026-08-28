---
name: reflect-workflow
description: Turn repeated lessons, user corrections, and reusable verification discoveries from completed work into evidence-backed improvements to the engineering workflow.
---

# Reflect Workflow

## Evidence gate

1. Use after a complex task, a costly dead end, a user correction, or a workflow that should be repeatable.
2. Skip trivial work, project-specific facts, and behavior already captured correctly.
3. Require either an explicit user preference, the same pattern across at least two tasks, or one high-impact failure with a clear prevention mechanism.

## Reflect

1. Reconstruct the task from the active record and final repository state.
2. Separate durable workflow lessons from implementation details that belong in project documentation.
3. For each candidate lesson, name the evidence, recurrence, failure it prevents, and existing rule it overlaps.
4. Prefer enforcement in tests, scripts, types, metadata, or runtime checks. Add prose only when structure cannot encode the lesson.
5. Update an existing skill before creating a new one. Create a new skill only when it has a distinct trigger and workflow.
6. Keep product-specific paths, private source, credentials, and conversation text out of portable instructions.

## Change control

1. When the user asked for reflection only, present proposed changes before editing the reusable stack.
2. When the user explicitly asked to improve the stack, apply only evidence-backed changes within that scope.
3. Validate every changed skill and the full plugin before completion.

Return accepted improvements, rejected candidates with reasons, validation evidence, and any backlog items that need more examples.
