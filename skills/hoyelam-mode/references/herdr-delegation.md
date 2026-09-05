# Herdr delegation adapter

Apply this adapter when the user requests Herdr orchestration. Hoyelam-mode still selects the workflow and verification depth; Herdr supplies worker terminals and their control surface.

## Route and bootstrap

1. Verify `HERDR_ENV=1` before inspecting or controlling the session. If it is absent, stop Herdr operations and report the boundary. Do not silently replace an explicitly requested Herdr route with native subagents.
2. Read the Herdr skill if it is available. Otherwise load the release-matched instructions with `herdr --skill`. Use `herdr --help` and the relevant command groups to confirm the installed syntax; do not run bare `herdr` inside a pane.
3. Keep the current agent as the lead. Use the smallest useful number of workers, with a default ceiling of three active workers across Herdr and native delegation combined. Honor lower configured limits; exceed the default only when the user or repository explicitly selects a larger concurrency profile.
4. Keep one owner for each assignment and mutable resource. Workers should report further delegation needs to the lead rather than start another worker tree. Do not assign the same unit through both routes.

## Brief and launch

1. Give each worker a self-contained brief with the goal, repository and working directory, applicable instructions and skill paths, relevant findings, writable and forbidden scope, acceptance criteria, evidence requirements, authorization boundaries, and report format. Separate CLI sessions do not inherit the lead's conversation or loaded skills.
2. Prefer independent read-heavy work. Concurrent writers need exclusive file boundaries or isolated worktrees and exclusive use of branches, simulators, and other mutable resources. If the allowed layout or checkout cannot support safe concurrent writes, serialize those units.
3. Follow the Herdr skill's layout rules: default to a sibling pane in the caller's tab and working directory, preserve focus with `--no-focus`, and use a different workspace, tab, worktree, or working directory only when requested. Resolve the caller with `--current` or its explicit identity; never infer it from UI focus.
4. Parse the new pane ID from the creation response. Start a uniquely named agent in the available shell pane with `herdr agent start <name> --kind <kind> --pane <pane-id>`. Honor the user's agent and model selection; otherwise use the lead's agent kind and the worker CLI's configured model. A new worker does not automatically inherit the lead's model. Native CLI arguments belong after `--`.
5. Record the worker name, pane ID, assigned scope, and attempt before sending work. Reuse an existing worker only when its identity, scope, and retained context fit the next assignment.

## Coordinate and verify

1. Submit the brief with `herdr agent prompt <target> <text>`. Use the installed CLI's wait support to wait for lifecycle changes while keeping useful lead work moving. Bound blocking waits so the lead can report progress; a timeout alone does not prove worker failure and is not a reason to resubmit the task.
2. Read results with `herdr agent get <target>` and `herdr agent read <target> --source recent-unwrapped --lines 120`. Resolve targets from recorded identities and current responses rather than sidebar order. Recheck identity after restarts or pane moves before sending further work.
3. Inspect a blocked worker's actual question or approval UI. Continue independent work and preserve existing authorization boundaries; do not answer an approval merely to advance the worker. Follow the Herdr skill and session instructions for any required user decision.
4. Treat `idle` or `done` as a signal to inspect a report, not proof that the assignment passed. `unknown`, a stalled prompt, or missing output is not completion. If terminal history cannot recover the full report, ask the worker to write it to a temporary Markdown file and read that file.
5. Require each worker to return `PASS`, `ISSUES`, or `BLOCKED`; the scope inspected or changed; commands and results; artifact paths and revision when applicable; findings distinguished from hypotheses; and remaining uncertainty or the next bounded action.
6. The lead reviews every accepted change, reconciles contradictory reports against live state, and runs the selected integration and verification checks. Herdr lifecycle status never substitutes for hoyelam-mode's completion rule.
7. Preserve panes and sessions the lead did not create. Do not stop the Herdr server as worker cleanup. Retain useful worker results before closing any task-owned pane.

## Project-scale records

When `$orchestrate-project` applies, keep its durable store, scope leases, assignment attempts, inbox, and revision-bound verification as the source of truth. Herdr does not replace those records.

Use the unique worker name as the assignment's worker identity and a session-qualified pane identity as its thread identity. Record both before prompting; do not use a pane ID alone across different Herdr sessions. Keep the stored worker, thread, and attempt on every report. Reconcile live occupants with the stored assignment on resume, and create a new assignment attempt when a worker is replaced. Persist the report and evidence before releasing the assignment.
