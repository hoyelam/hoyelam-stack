# Automations

## Full quality pass

Use after implementation when a branch needs the complete hoyelam-stack finish line:

1. Read `automations/full-quality-pass/FOR_AGENTS.md`.
2. Configure the repository and branch in the automation editor.
3. Keep the pack dormant until the user explicitly enables it.
4. The automation may resolve verified branch findings but may not merge or deploy.

## Pull request quality watch

Use when an existing pull request should remain review-ready:

1. Read `automations/pr-quality-watch/FOR_AGENTS.md`.
2. Configure the repository and pull request selection rule.
3. Verify `gh` authentication and repository write permission before allowing fixes.
4. The automation may diagnose CI and review feedback, push in-scope fixes, and update the pull request summary.
5. It may not approve, merge, release, deploy, or dismiss human feedback.

## Workflow reflection

Use to review completed work for improvements to the reusable stack:

1. Read `automations/workflow-reflection/FOR_AGENTS.md`.
2. Configure the exact task set, repositories, time window, and proposal output.
3. Require explicit preferences, repeated evidence, or one high-impact preventable failure.
4. Produce proposals by default; edit the reusable stack only when explicitly authorized.
5. Keep project source and private conversation text out of portable instructions.

## Shared boundary

1. Use repository-local instructions and verification commands.
2. Fail closed on ambiguous repository, branch, permissions, or destructive worktree state.
3. Do not post external messages unless the configured automation explicitly authorizes the destination and message.
4. Report unchanged state concisely.
