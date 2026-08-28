# Releases

## Version contract

1. Use semantic versions for public releases.
2. Keep `plugin.json` and `.codex-plugin/plugin.json` on the same version.
3. Set the repository marketplace source ref to `v<version>`.
4. Validate the repository, skills, plugin manifest, and marketplace before committing.
5. Create one release commit, an annotated matching tag, and a GitHub release.
6. Push the release commit before its tag so the marketplace never points at an unpublished commit.

The repository marketplace is the supported distribution channel. Publication to a universal plugin directory is not part of this process.

## Consumer updates

1. Run `codex plugin marketplace upgrade hoyelam`.
2. Run `codex plugin add hoyelam-stack@hoyelam`.
3. Start a new Codex task.

## Source installations

Source installations follow the checked-out branch or tag. Pull `main` for current development or check out a release tag for a stable version.
