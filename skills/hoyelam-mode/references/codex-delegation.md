# Codex delegation adapter

Apply this adapter only when Codex exposes subagent tools and delegation is authorized by the user, repository instructions, or the active skill.

## Route

1. Treat three active children as the hoyelam-stack default ceiling, not a universal Codex limit. Honor a lower runtime or configured cap. Exceed three only when the user or repository explicitly selects a larger Codex concurrency profile and the extra independent streams justify it.
2. Keep the parent active for metadata discovery, decisions, integration, verification, and user reporting. Capacity is a ceiling, not a target.
3. Prefer read-heavy evidence streams. Give concurrent writers exclusive worktrees, branches, files, simulators, or mutable resources.

## Fork

1. Use the smallest positive `fork_turns` value that includes the relevant recent request and decisions.
2. Use `fork_turns: "none"` only when the brief is fully self-contained. Use `fork_turns: "all"` only when the complete history is materially required.
3. Include discovered repository instructions, exact scope, acceptance criteria, required evidence, forbidden actions, and report shape in the brief. Do not ask a child to rediscover parent-owned metadata.

## Reuse and control

1. Reuse an idle child with `followup_task` when its established role and context fit the next bounded stream. Spawn a new child when reuse would carry misleading context or a conflicting scope.
2. Use `send_message` for a correction to running work. Use `interrupt_agent` only when the current work is wrong, unsafe, or no longer needed.
3. Wait with `wait_agent` instead of polling. Keep useful parent work moving while children run.

## Report

Every child returns:

1. Status: `PASS`, `ISSUES`, or `BLOCKED`.
2. Scope inspected or changed.
3. Evidence collected, including commands, artifacts, file and symbol references, and revision when applicable.
4. Findings and contradictions, separated from hypotheses.
5. Remaining uncertainty and the next bounded action when blocked.

The parent reports the routing choice, reconciles child results against live state, and never forwards raw child output as its own conclusion.
