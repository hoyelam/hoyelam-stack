# Comment policy

## Default decision

Delete the comment and make the code carry the meaning.

## Exceptions

1. Keep legal and license headers.
2. Keep a proven external constraint only when names, types, tests, runtime checks, or tooling cannot express it.
3. Keep required formatter or generator directives only when their effect is verified.

## Prefix contract

1. `IMPORTANT` identifies an externally imposed invariant.
2. `DO NOT REMOVE` identifies a specific externally imposed failure caused by removal.
3. `TOO RISKY` records a rejected alternative with current evidence of unacceptable risk.
4. `FINE FOR NOW` records a bounded temporary tradeoff and its removal condition.

Every prefixed comment must answer:

1. What external system imposes this?
2. Where is the evidence?
3. What fails if the code changes?
4. When can the comment be removed?

## Review decisions

1. Delete narration, banners, repetition, commented-out code, stale tasks, and workaround history.
2. Reshape confusing internal code instead of explaining it.
3. Replace suppressions with a real fix when the rule protects correctness or safety.
4. Encode durable constraints as tests, types, assertions, generators, or CI checks.
5. Revalidate old external constraints against current documentation or runtime behavior.

## Rare acceptable shape

`IMPORTANT: WebKit requires this call on the main actor; removing the hop reproduces vendor issue 1234 on macOS 15. Remove after the minimum deployment target excludes macOS 15.`

The prefix does not make this acceptable. The current vendor constraint, reproduction, and removal condition do.
