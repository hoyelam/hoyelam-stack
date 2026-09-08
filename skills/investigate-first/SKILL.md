---
name: investigate-first
description: Find the supported cause and owning boundary of a defect or unfamiliar subsystem.
---

# Investigate First

Establish expected and observed behavior, relevant constraints, and what would resolve the question. Locate the owning repository and read its instructions, source, direct callers, tests, and relevant architecture. Follow evidence to the smallest boundary that explains the behavior.

Reproduce the symptom when practical. Use logs, traces, persisted state, or a focused invocation to distinguish a cause from a plausible source-only explanation. Consult history when a regression or earlier design decision matters. Identify the important assumption that makes a proposed change safe, and check it through source or executable evidence where possible.

For repeated remote-source research, [source research](references/source-research.md) provides an optional cache helper with explicit revisions. Use it when reuse helps; ordinary local searches need no extra tool. For timing failures, [condition-based observation](references/condition-based-observation.md) describes a bounded readiness check.

Report the supported cause or strongest remaining hypothesis, its evidence, affected boundary, and next useful action. Expand the explanation only where uncertainty or impact needs it. Investigation remains read-only unless implementation is authorized.
