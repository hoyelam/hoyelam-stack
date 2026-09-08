# Condition-based observation

Use when startup, asynchronous effects, or intermittent failures make a fixed delay unreliable.

Identify the observable condition the next action depends on: a service response, accessible control, persisted value, or process state. Prefer the project's existing wait/assertion API. Bound it with a deadline and retain the last observed state on failure. Readiness is a prerequisite; separately assert the feature's result.

For a failure, trace the incorrect value or state backward through its callers and side effects until evidence identifies where it diverged from the intended contract. Change the owning boundary, then re-exercise the original path. Increasing a sleep or timeout alone needs evidence that the expected behavior legitimately requires it.
