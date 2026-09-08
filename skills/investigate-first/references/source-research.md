# Optional source repository cache

Use this helper when repeated source research would benefit from a local checkout. For a small one-off lookup, existing repository or GitHub CLI reads are sufficient.

It requires Python 3 and Git on macOS or Linux, plus GitHub CLI for GitHub clones. Resolve `<investigate-first-skill>` to this skill's discovered directory; the script path is independent of the project working directory.

```bash
python3 <investigate-first-skill>/scripts/reference_repo.py https://github.com/OWNER/REPO --ref main
python3 <investigate-first-skill>/scripts/reference_repo.py /path/to/local/repository --ref COMMIT_SHA --cache-dir /tmp/reference-repos
```

For GitHub network access, first follow the session's GitHub CLI authentication checks and sandbox retry policy. The helper uses `gh repo clone` for an initial GitHub clone and native `git fetch` for refresh, which has no equivalent GitHub CLI operation. It does not log in, inspect tokens, or change credentials. Other explicit HTTPS or SSH repository URLs use Git transport unchanged. GitHub shorthand and blob/tree URLs are rejected: pass the repository URL and an explicit `--ref` separately.

Success prints JSON containing the requested ref, actual immutable `revision`, detached checkout `path`, `cache_status` (`created`, `reused`, or `refreshed`), and `snapshot_status`. Record the revision with research evidence and use it for source permalinks. A branch or tag describes a moving reference; a full commit SHA keeps later requests pinned to the same revision.

The cache defaults to `~/.cache/hoyelam-stack/reference-repos`. Its directory key hashes the explicit source URL or resolved local path; different URL spellings may create separate entries. Branches and tags refresh at most once per 300 seconds by default. Use `--refresh` for an immediate fetch or `--refresh-interval SECONDS` to change the interval. Full commit pins reuse cached objects without an automatic fetch. Commands and lock waits have a bounded timeout, configurable with `--timeout`.

Each commit gets its own detached worktree. Local source repositories are only read; only committed content is cached. Existing snapshot changes, including untracked and ignored files, cause an error instead of being overwritten. Use a separate workspace for edits. If a snapshot is dirty or cache metadata is damaged, preserve it and choose a different `--cache-dir`; the helper never resets or cleans it for you. Failed refreshes return an error instead of silently presenting stale results as current.

Use `rg` and normal file reads in the returned path. Submodules are not initialized. Large files managed by external filters may need the project's normal tooling. Cache directories accumulate until you remove unused entries after checking for local changes; there is no automatic eviction.
