# Worker brief

Give the worker enough context to execute one independent outcome without repeating the lead's broad discovery. A short brief can cover:

- **Outcome and context:** the goal, repository and owning surface, applicable instructions, relevant findings, and dependency outputs the worker needs.
- **Scope and authority:** owned writable paths or resources, forbidden actions, and any shared-state isolation constraint.
- **Acceptance and proof:** observable criteria, required checks or interactions, prerequisites, expected results, and evidence to return. Distinguish optional checks and known blockers.
- **Return:** actual changes or findings, tested artifact, commands and observations, unresolved issues, and the next bounded action when blocked.

For a continuing program, include current standing decisions. Add worker/session identity and attempt numbers when retries or interruption require durable correlation. When selecting the bundled runtime, record assignment identities and canonical [scope leases](scope-leases.md) before writes. Add a timebox or stopping condition when work could otherwise continue without useful progress.

Send current dependency evidence or a readable artifact containing it; a unit name alone carries ordering, not context.
