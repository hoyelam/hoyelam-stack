# Worker brief

Use the smallest version of this contract that still prevents guessing.

1. `GOAL`: one observable outcome executable without access to the coordinator conversation.
2. `SCOPE`: writable paths or resources, forbidden paths or resources, and the exclusive worktree or branch when applicable.
3. `CONTEXT`: repository instructions, owning files, architecture decisions, dependency results, and relevant failure evidence.
4. `ACCEPTANCE`: independently checkable criteria, one per line.
5. `VERIFY`: exact commands or runtime interactions, prerequisites, expected observations, required versus optional checks, artifact identity, evidence to preserve, and known environmental limits. For runtime work include relevant harness identity and user paths; bundled feature-map and doctor fields apply only when that format is used.
6. `DEPENDENCIES`: unit identifiers whose outputs must be relayed before work begins.
7. `TIMEBOX`: a stopping condition that returns partial evidence instead of continuing indefinitely.
8. `FORBIDDEN`: destructive operations, external mutations, scope expansion, and unit-specific restrictions.
9. `ASSIGNMENT`: worker name, runtime session identity, attempt number, and exclusive ownership of every writable or mutable boundary. When using the bundled runtime, use canonical lease keys from [scope-leases.md](scope-leases.md).
10. `REPORT`: status, assignment identity, revision or artifact identifier, changed paths, evidence actually collected, deviations, blockers, and suggested follow-ups.
11. `STANDING`: the complete current standing-order list.

Dependencies carry context as well as ordering. Paste the relevant upstream result into the downstream brief or point to a durable repository artifact the worker can read.
