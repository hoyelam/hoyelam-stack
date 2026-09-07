# Single-task delegation

Read before delegating a bounded task under hoyelam-mode.

1. Keep task framing, repository and instruction discovery, worktree state, architecture selection, decomposition, authorization boundaries, and final integration in the parent.
2. Delegate only a meaningful evidence stream: a bounded investigation, specialist review, test or log analysis, documentation check, or independent implementation unit whose result can change the parent decision or materially reduce elapsed time.
3. Do not delegate metadata discovery, one obvious command, clerical restatement, tightly sequential reasoning, or shared writes that cost more to coordinate than to perform directly.
4. Give each child one independent goal, the relevant discovered context, an exclusive scope, exact evidence requirements, and a compact report contract. The child should not repeat the parent's broad repository survey.
5. Use the smallest useful number of children. Run `scripts/delegation_router.py --help` when the `0–3` route is not obvious.
6. The parent owns synthesis, verifies material claims, resolves contradictions, reviews every accepted change, and reports one integrated result.
7. Select the execution route only after deciding delegation is useful and authorized. Honor explicit user preferences, including native delegation or no delegation. Otherwise, when `HERDR_ENV=1` and the Herdr CLI is available, read [references/herdr-delegation.md](herdr-delegation.md), check the managed session with its read-only bootstrap steps, and automatically use Herdr when reachable. An explicit Herdr request also uses that adapter; no repeated orchestration prompt is needed for automatic selection.
8. Outside Herdr, or when automatic detection finds its CLI or managed session unavailable, use native delegation when available and authorized; in Codex, read [references/codex-delegation.md](codex-delegation.md) first. Briefly report a failed automatic Herdr check and the selected fallback. If the user explicitly requires Herdr, report the blocker instead of silently switching routes. When no route is available, continue useful direct work. Keep one parent responsible for assignments and integration across either route.

