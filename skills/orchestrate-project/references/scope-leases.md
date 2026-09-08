# Scope leases

Use these keys when the bundled runtime manages assignments. Other coordination tools may preserve exclusive ownership using their own conventions.

## Format

1. Every lease uses `<namespace>:<resource>`.
2. The namespace starts with a lowercase letter and contains only lowercase letters, digits, and hyphens.
3. Repeat `--lease` for every independently mutable boundary owned by the attempt.
4. Lease identity is stable across retries. Release the current attempt before another attempt reacquires its leases.

## Repository paths

1. Use `repo:.` for the entire repository.
2. Use `repo:<relative-path>` for a file or directory, with `/` separators.
3. Repository paths must not be absolute or contain empty, `.`, or `..` segments.
4. Repository leases conflict when either path is the same as or an ancestor of the other. `repo:Sources` conflicts with `repo:Sources/Feature.swift`; `repo:Sources` does not conflict with `repo:Tests`.

## Other resources

Other namespaces are opaque and conflict on exact equality. Use one canonical identifier for a simulator, branch, worktree, external account, or other mutable resource. Examples include `simulator:DEVICE-UDID`, `branch:repository#feature-name`, and `account:service#staging`.
