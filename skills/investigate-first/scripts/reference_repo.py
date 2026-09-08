#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import math
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlsplit


class CacheError(Exception):
    pass


def run(arguments: list[str], timeout: int) -> str:
    environment = os.environ.copy()
    for name in (
        "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
        "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    ):
        environment.pop(name, None)
    environment["GIT_TERMINAL_PROMPT"] = "0"
    try:
        with subprocess.Popen(
            arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            env=environment, start_new_session=True,
        ) as process:
            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired as error:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.communicate()
                raise CacheError(f"{arguments[0]} exceeded {timeout}s; retry when the source is reachable") from error
    except OSError as error:
        raise CacheError(f"Could not run {arguments[0]}: {error}") from error
    if process.returncode:
        detail = stderr.strip() or stdout.strip() or "no diagnostic output"
        raise CacheError(f"{arguments[0]} exited {process.returncode}: {detail}")
    return stdout.strip()


def git(arguments: list[str], timeout: int) -> str:
    return run([
        "git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
        "-c", "protocol.ext.allow=never", *arguments,
    ], timeout)


def resolve_source(source: str) -> tuple[str, bool, bool]:
    if "://" not in source:
        path = Path(source).expanduser()
        if not path.exists():
            raise CacheError("Use an existing local repository path or an explicit https:// or ssh:// repository URL")
        return str(path.resolve()), False, False
    parsed = urlsplit(source)
    if parsed.scheme not in ("https", "ssh") or not parsed.hostname:
        raise CacheError("Remote repositories require an explicit https:// or ssh:// URL")
    if parsed.query or parsed.fragment or parsed.password or (parsed.scheme == "https" and parsed.username):
        raise CacheError("Use a repository URL without credentials, query, or fragment; supply the revision with --ref")
    github = parsed.hostname.lower() == "github.com"
    if github and len(parsed.path.strip("/").split("/")) != 2:
        raise CacheError("Use the GitHub repository URL (owner/repo), without blob/tree paths, and supply --ref separately")
    return source, True, github


def clone_command(source: str, destination: Path, remote: bool, github: bool) -> list[str]:
    if github:
        return ["gh", "repo", "clone", source, str(destination), "--", "--bare", "--filter=blob:none"]
    arguments = ["git", "clone", "--bare", "--no-hardlinks"]
    if remote:
        arguments.append("--filter=blob:none")
    return [*arguments, "--", source, str(destination)]


@contextmanager
def cache_lock(path: Path, timeout: int):
    with path.open("a") as lock:
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise CacheError("Another process is using this repository cache; retry after it finishes")
                time.sleep(0.05)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def save_state(path: Path, source: str) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps({"source": source, "refreshed_at": time.time()}))
    temporary.replace(path)


def cached_repository(arguments: argparse.Namespace) -> dict[str, object]:
    source, remote, github = resolve_source(arguments.repository)
    ref = arguments.ref
    if ref.startswith("-") or ref.startswith("/"):
        raise CacheError("--ref must be a branch, tag, full ref name, or full commit SHA")
    try:
        git(["check-ref-format", "--allow-onelevel", ref], arguments.timeout)
    except CacheError as error:
        raise CacheError("--ref must be a branch, tag, full ref name, or full commit SHA; revision expressions are unsupported") from error
    pinned = re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", ref) is not None
    cache = arguments.cache_dir.expanduser().resolve() / hashlib.sha256(source.encode()).hexdigest()
    if cache.is_symlink():
        raise CacheError(f"Unexpected cache symlink at {cache}; use a different --cache-dir")
    cache.mkdir(parents=True, exist_ok=True)
    repository = cache / "repository.git"
    state_path = cache / "state.json"
    with cache_lock(cache / "lock", arguments.timeout):
        if repository.is_symlink() or (cache / "snapshots").is_symlink():
            raise CacheError(f"Unexpected symlink inside {cache}; preserve it and use a different --cache-dir")
        status = "reused"
        if repository.exists():
            try:
                state = json.loads(state_path.read_text())
                refreshed_at = float(state["refreshed_at"])
                if state["source"] != source or not math.isfinite(refreshed_at):
                    raise ValueError("repository source does not match")
            except (OSError, ValueError, KeyError, TypeError) as error:
                raise CacheError(f"Invalid cache metadata at {state_path}; preserve this cache and use a different --cache-dir") from error
            if git(["--git-dir", str(repository), "rev-parse", "--is-bare-repository"], arguments.timeout) != "true":
                raise CacheError(f"Expected a bare repository at {repository}; use a different --cache-dir")
            age = time.time() - refreshed_at
            if arguments.refresh or (not pinned and (age < 0 or age >= arguments.refresh_interval)):
                git([
                    "--git-dir", str(repository), "fetch", "--prune", "origin",
                    "+refs/heads/*:refs/heads/*", "+refs/tags/*:refs/tags/*",
                ], arguments.timeout)
                save_state(state_path, source)
                status = "refreshed"
        else:
            if state_path.exists():
                raise CacheError(f"Incomplete cache at {cache}; preserve it and use a different --cache-dir")
            with tempfile.TemporaryDirectory(prefix="clone-", dir=cache) as temporary:
                clone = Path(temporary) / "repository.git"
                command = clone_command(source, clone, remote, github)
                if command[0] == "git":
                    git(command[1:], arguments.timeout)
                else:
                    run(command, arguments.timeout)
                clone.rename(repository)
            save_state(state_path, source)
            status = "created"
        try:
            resolved_ref = ref.lower() if pinned else git([
                "--git-dir", str(repository), "rev-parse", "--symbolic-full-name", "--verify", "--end-of-options", ref,
            ], arguments.timeout)
            if not pinned and not resolved_ref.startswith(("refs/heads/", "refs/tags/")):
                raise CacheError("Use an unambiguous branch/tag name, a full refs/heads/ or refs/tags/ name, or a full commit SHA")
            revision = git([
                "--git-dir", str(repository), "rev-parse", "--verify", "--end-of-options", f"{resolved_ref}^{{commit}}",
            ], arguments.timeout)
        except CacheError as error:
            raise CacheError(f"Requested ref {ref!r} is unavailable; check the name or retry with --refresh. {error}") from error
        snapshot = cache / "snapshots" / revision
        snapshot_status = "reused"
        if snapshot.exists() or snapshot.is_symlink():
            if snapshot.is_symlink() or git(["-C", str(snapshot), "rev-parse", "HEAD"], arguments.timeout) != revision:
                raise CacheError(f"Snapshot no longer matches {revision}: {snapshot}; preserve it and use a different --cache-dir")
            if git(["-C", str(snapshot), "rev-parse", "--abbrev-ref", "HEAD"], arguments.timeout) != "HEAD":
                raise CacheError(f"Snapshot is no longer detached: {snapshot}; preserve it and use a different --cache-dir")
            changes = git([
                "-C", str(snapshot), "status", "--porcelain=v1", "--untracked-files=all", "--ignored",
            ], arguments.timeout)
            if changes:
                raise CacheError(f"Snapshot has local changes: {snapshot}; preserve your files and use a different --cache-dir")
        else:
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            git([
                "--git-dir", str(repository), "worktree", "add", "--detach", str(snapshot), revision,
            ], arguments.timeout)
            snapshot_status = "created"
        return {
            "repository": source,
            "requested_ref": ref,
            "revision": revision,
            "path": str(snapshot),
            "cache_status": status,
            "snapshot_status": snapshot_status,
        }


def bounded_integer(minimum: int, maximum: int):
    def parse(value: str) -> int:
        try:
            number = int(value)
        except ValueError as error:
            raise argparse.ArgumentTypeError("expected an integer") from error
        if not minimum <= number <= maximum:
            raise argparse.ArgumentTypeError(f"expected a value between {minimum} and {maximum}")
        return number
    return parse


def main() -> int:
    parser = argparse.ArgumentParser(description="Cache a reference repository and report a clean detached snapshot as JSON")
    parser.add_argument("repository", help="explicit repository URL or existing local repository path")
    parser.add_argument("--ref", required=True, help="branch, tag, full ref name, or full commit SHA; no revision expressions")
    parser.add_argument("--cache-dir", type=Path, default=Path.home() / ".cache" / "hoyelam-stack" / "reference-repos")
    parser.add_argument("--refresh", action="store_true", help="fetch now, including for a full commit SHA")
    parser.add_argument("--refresh-interval", type=bounded_integer(0, 86400), default=300, help="seconds between branch/tag refreshes (default: 300)")
    parser.add_argument("--timeout", type=bounded_integer(1, 300), default=60, help="maximum seconds per command and lock wait (default: 60)")
    arguments = parser.parse_args()
    try:
        print(json.dumps(cached_repository(arguments), sort_keys=True))
    except (CacheError, OSError, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
