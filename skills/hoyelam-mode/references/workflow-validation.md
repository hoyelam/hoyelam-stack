# Validate workflow behavior

Use this when changing the stack's behavioral rules. Structural checks prove packaging and helper behavior; realistic tasks provide evidence of how an agent applies the instructions. Keep the size of the exercise proportionate to the change.

1. Before running tasks, define observable criteria for the behavior being changed. Useful criteria include a verification plan before edits, reproduction through the owning interface, meaningful assertions, verification after review fixes, scope preservation, and honest reporting of blocked checks.
2. Prepare small isolated projects with ordinary source, repository instructions, and supported commands. Include successful implementation and an unavailable required check when completion rules changed. Preserve starting files so another reviewer can compare the actual changes.
3. Give each worker an ordinary user request and the workflow variant in use. Keep the scoring criteria, expected implementation, planted failure mechanism, and other workers' results out of its brief. Do not ask workers to describe how they would behave instead of doing the work.
4. Keep mutable state isolated and use only authorized local actions. Delegate when available and authorized; otherwise report the absence of independent execution rather than presenting self-review as such.
5. Inspect actual edits and command results, and independently rerun relevant checks. Review available task-local tool activity for ordering claims such as planning before editing; if activity is unavailable, mark that criterion unobserved. A worker's claimed compliance is insufficient.
6. For review-and-resolution behavior, include a supported review finding and inspect the resulting fix and affected rerun. Distinguish a natural finding from a deliberately supplied one. Do not invent a finding just to claim the loop was exercised.
7. Record the workflow version or content hashes, starting state, requests, observed outcomes, evidence locations, and limitations. Keep worker execution results separate from the reviewer's assessment. Do not claim improvement over an earlier variant without a comparable baseline.
8. Correct only demonstrated in-scope gaps, then rerun affected tasks against the changed guidance. Report the task-specific evidence; a small exercise cannot establish reliability across all projects or agents.
