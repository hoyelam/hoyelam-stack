#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import stat
import sys
import tempfile
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Iterator


UNIT_STATES = {"pending", "running", "verification", "blocked", "done", "abandoned"}
TERMINAL_STATES = {"done", "abandoned"}
VERDICTS = {"verified", "failed", "blocked"}
ATTEMPT_OUTCOMES = {"completed", "blocked", "failed", "cancelled"}
DOCTOR_STATUSES = {"passed", "failed", "not-run"}
SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
LEASE_NAMESPACE = re.compile(r"^[a-z][a-z0-9-]*$")


class OrchestratorError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default: object) -> object:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise OrchestratorError(f"invalid JSON in {path}: {error}") from error


def require_runtime_directory(path: Path, create: bool) -> bool:
    if create:
        try:
            path.mkdir(exist_ok=True)
        except OSError as error:
            raise OrchestratorError(f"cannot create runtime temporary directory {path}: {error}") from error
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    except OSError as error:
        raise OrchestratorError(f"cannot inspect runtime temporary directory {path}: {error}") from error
    if not stat.S_ISDIR(mode):
        raise OrchestratorError(f"runtime temporary path is not a real directory: {path}")
    return True


def atomic_write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_directory = path.parent / ".hoyelam-tmp"
    require_runtime_directory(temporary_directory, create=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f"{path.name}.", dir=temporary_directory)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(contents)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def write_json(path: Path, value: object) -> None:
    atomic_write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def require_identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or not SAFE_IDENTIFIER.fullmatch(value):
        raise OrchestratorError(f"{label} must match {SAFE_IDENTIFIER.pattern}")
    return value


def require_string(value: object, label: str, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise OrchestratorError(f"{label} must be a string")
    if not allow_empty and not value.strip():
        raise OrchestratorError(f"{label} must be a non-empty string")
    return value


def require_text(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise OrchestratorError(f"{label} must be one non-empty line")
    normalized = value.strip()
    if not normalized or "\n" in normalized or "\r" in normalized:
        raise OrchestratorError(f"{label} must be one non-empty line")
    return normalized


def require_text_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list):
        raise OrchestratorError(f"{label} must be a list")
    result = [require_text(item, f"{label} item") for item in value]
    if len(result) != len(set(result)):
        raise OrchestratorError(f"{label} must not contain duplicates")
    return result


def canonicalize_lease(value: str) -> str:
    normalized = require_text(value, "scope lease")
    namespace, separator, resource = normalized.partition(":")
    if not separator or not LEASE_NAMESPACE.fullmatch(namespace) or not resource:
        raise OrchestratorError("scope lease must use <namespace>:<resource>")
    if namespace != "repo":
        return normalized
    if resource == ".":
        return normalized
    if resource.startswith("/") or "\\" in resource:
        raise OrchestratorError("repo scope lease must use a POSIX repository-relative path")
    parts = resource.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise OrchestratorError("repo scope lease path must already be canonical")
    return f"repo:{PurePosixPath(*parts)}"


def leases_overlap(left: str, right: str) -> bool:
    if left == right:
        return True
    left_namespace, _, left_resource = left.partition(":")
    right_namespace, _, right_resource = right.partition(":")
    if left_namespace != "repo" or right_namespace != "repo":
        return False
    if left_resource == "." or right_resource == ".":
        return True
    left_parts = PurePosixPath(left_resource).parts
    right_parts = PurePosixPath(right_resource).parts
    shared_length = min(len(left_parts), len(right_parts))
    return left_parts[:shared_length] == right_parts[:shared_length]


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


class Store:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.program_path = self.root / "program.json"
        self.units_path = self.root / "units.json"
        self.verification_path = self.root / "verification.json"
        self.gates_path = self.root / "gates.json"
        self.pending_inbox = self.root / "inbox" / "pending"
        self.processed_inbox = self.root / "inbox" / "processed"
        self.status_path = self.root / "status.md"
        self.standing_orders_path = self.root / "standing-orders.md"
        self.lock_path = self.root / ".lock"

    @contextmanager
    def locked(self) -> Iterator[None]:
        self.root.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                self.cleanup_temporary_files_unlocked()
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def cleanup_temporary_files_unlocked(self) -> None:
        directories = (self.root / ".hoyelam-tmp", self.pending_inbox / ".hoyelam-tmp")
        for directory in directories:
            if not require_runtime_directory(directory, create=False):
                continue
            for path in directory.iterdir():
                if not path.is_file():
                    raise OrchestratorError(f"runtime temporary directory contains a non-file entry: {path}")
                try:
                    path.unlink()
                except OSError as error:
                    raise OrchestratorError(f"cannot remove orphan temporary file {path}: {error}") from error

    def require_initialized(self) -> None:
        if not self.program_path.is_file():
            raise OrchestratorError(f"store is not initialized: {self.root}")

    def require_active(
        self,
    ) -> tuple[
        dict[str, object],
        dict[str, dict[str, object]],
        list[dict[str, object]],
        dict[str, dict[str, object]],
        list[dict[str, object]],
    ]:
        state = self.validate_store_unlocked()
        if state[0].get("status") != "active":
            raise OrchestratorError("program is closed and cannot be mutated")
        return state

    def program(self) -> dict[str, object]:
        value = read_json(self.program_path, {})
        if not isinstance(value, dict):
            raise OrchestratorError("program.json must contain an object")
        required = {"goal", "done_predicate", "status", "created_at", "completed_at"}
        missing = sorted(required - value.keys())
        if missing:
            raise OrchestratorError(f"program.json is missing fields: {', '.join(missing)}")
        require_string(value["goal"], "stored program goal")
        require_string(value["done_predicate"], "stored done predicate")
        status = value["status"]
        if not isinstance(status, str) or status not in {"active", "complete"}:
            raise OrchestratorError(f"stored program status is invalid: {status}")
        require_text(value["created_at"], "stored program creation time")
        completed_at = value["completed_at"]
        if completed_at is not None:
            require_text(completed_at, "stored program completion time")
        if status == "active" and completed_at is not None:
            raise OrchestratorError("active program must not have a completion time")
        if status == "complete" and completed_at is None:
            raise OrchestratorError("complete program requires a completion time")
        return value

    def validate_assignment_identity(self, value: object, label: str) -> dict[str, object]:
        if not isinstance(value, dict):
            raise OrchestratorError(f"{label} must contain an object")
        required = {"worker", "thread", "attempt", "leases", "assigned_at"}
        missing = sorted(required - value.keys())
        if missing:
            raise OrchestratorError(f"{label} is missing fields: {', '.join(missing)}")
        worker = require_text(value["worker"], f"{label} worker")
        thread = require_text(value["thread"], f"{label} thread")
        attempt = value["attempt"]
        if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
            raise OrchestratorError(f"{label} attempt must be a positive integer")
        lease_values = value["leases"]
        if not isinstance(lease_values, list) or not lease_values:
            raise OrchestratorError(f"{label} leases must contain a non-empty list")
        leases = [canonicalize_lease(item) for item in lease_values]
        if leases != sorted(set(leases)):
            raise OrchestratorError(f"{label} leases must be unique, sorted, and canonical")
        assigned_at = require_text(value["assigned_at"], f"{label} assignment time")
        return {
            "worker": worker,
            "thread": thread,
            "attempt": attempt,
            "leases": leases,
            "assigned_at": assigned_at,
        }

    def units(self) -> dict[str, dict[str, object]]:
        value = read_json(self.units_path, {})
        if not isinstance(value, dict) or not all(isinstance(item, dict) for item in value.values()):
            raise OrchestratorError("units.json must contain an object of unit objects")
        required = {
            "id",
            "state",
            "revision",
            "goal",
            "scope",
            "acceptance",
            "verify",
            "depends_on",
            "created_at",
            "updated_at",
        }
        for identifier, unit in value.items():
            require_identifier(identifier, "stored unit key")
            missing = sorted(required - unit.keys())
            if missing:
                raise OrchestratorError(f"stored unit {identifier} is missing fields: {', '.join(missing)}")
            if require_identifier(unit["id"], "stored unit identifier") != identifier:
                raise OrchestratorError(f"stored unit identifier does not match its key: {identifier}")
            state = unit["state"]
            if not isinstance(state, str) or state not in UNIT_STATES:
                raise OrchestratorError(f"stored unit state is invalid: {identifier} ({state})")
            revision = require_string(unit["revision"], f"stored unit revision for {identifier}", allow_empty=True)
            if revision:
                require_text(revision, f"stored unit revision for {identifier}")
            if state == "done":
                require_text(revision, f"stored done-unit revision for {identifier}")
            for field in ("goal", "scope", "acceptance", "verify"):
                require_string(unit[field], f"stored unit {field} for {identifier}")
            dependencies = unit["depends_on"]
            if not isinstance(dependencies, list):
                raise OrchestratorError(f"stored unit dependencies must contain a list: {identifier}")
            normalized_dependencies = [
                require_identifier(dependency, f"stored dependency for {identifier}")
                for dependency in dependencies
            ]
            if len(normalized_dependencies) != len(set(normalized_dependencies)) or identifier in normalized_dependencies:
                raise OrchestratorError(f"stored unit dependencies are invalid: {identifier}")
            require_text(unit["created_at"], f"stored unit creation time for {identifier}")
            require_text(unit["updated_at"], f"stored unit update time for {identifier}")
            attempts = unit.setdefault("attempts", [])
            assignment = unit.setdefault("assignment", None)
            if not isinstance(attempts, list):
                raise OrchestratorError(f"unit attempts must contain a list of objects: {identifier}")
            identities: list[dict[str, object]] = []
            for index, attempt_record in enumerate(attempts, start=1):
                if not isinstance(attempt_record, dict):
                    raise OrchestratorError(f"stored unit attempt must contain an object: {identifier}#{index}")
                attempt_required = {"started_at", "ended_at", "outcome"}
                attempt_missing = sorted(attempt_required - attempt_record.keys())
                if attempt_missing:
                    raise OrchestratorError(
                        f"stored unit attempt {identifier}#{index} is missing fields: {', '.join(attempt_missing)}"
                    )
                identity = self.validate_assignment_identity(
                    attempt_record,
                    f"stored unit attempt {identifier}#{index}",
                )
                if identity["attempt"] != index:
                    raise OrchestratorError(f"stored unit attempts must be contiguous: {identifier}")
                require_text(attempt_record.get("started_at"), f"stored attempt start time for {identifier}#{index}")
                ended_at = attempt_record.get("ended_at")
                outcome = attempt_record.get("outcome")
                if outcome is None:
                    if ended_at is not None:
                        raise OrchestratorError(f"unfinished attempt must not have an end time: {identifier}#{index}")
                    if index != len(attempts):
                        raise OrchestratorError(f"only the latest attempt may be unfinished: {identifier}#{index}")
                else:
                    if not isinstance(outcome, str) or outcome not in ATTEMPT_OUTCOMES:
                        raise OrchestratorError(f"stored attempt outcome is invalid: {identifier}#{index}")
                    require_text(ended_at, f"stored attempt end time for {identifier}#{index}")
                identities.append(identity)
            if assignment is not None:
                active_identity = self.validate_assignment_identity(
                    assignment,
                    f"stored active assignment for {identifier}",
                )
                if not identities or active_identity != identities[-1]:
                    raise OrchestratorError(f"active assignment does not match the latest attempt: {identifier}")
                latest_attempt = attempts[-1]
                if latest_attempt.get("outcome") is not None or latest_attempt.get("ended_at") is not None:
                    raise OrchestratorError(f"active assignment points to a finished attempt: {identifier}")
                if state != "running":
                    raise OrchestratorError(f"active assignment requires running state: {identifier}")
            elif attempts and attempts[-1].get("outcome") is None:
                raise OrchestratorError(f"unfinished attempt has no active assignment: {identifier}")
        for identifier, unit in value.items():
            unknown = sorted(str(item) for item in unit["depends_on"] if str(item) not in value)
            if unknown:
                raise OrchestratorError(f"stored unit has unknown dependencies: {identifier} ({', '.join(unknown)})")
        return value

    def verification(self) -> list[dict[str, object]]:
        value = read_json(self.verification_path, [])
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            raise OrchestratorError("verification.json must contain a list")
        identities: set[tuple[str, str]] = set()
        required = {"unit", "revision", "verdict", "evidence", "recorded_at"}
        for index, row in enumerate(value, start=1):
            missing = sorted(required - row.keys())
            if missing:
                raise OrchestratorError(f"stored verification {index} is missing fields: {', '.join(missing)}")
            unit = require_identifier(row["unit"], f"stored verification unit {index}")
            revision = require_text(row["revision"], f"stored verification revision {index}")
            verdict = row["verdict"]
            if not isinstance(verdict, str) or verdict not in VERDICTS:
                raise OrchestratorError(f"stored verification verdict is invalid: {index}")
            require_string(row["evidence"], f"stored verification evidence {index}")
            require_text(row["recorded_at"], f"stored verification time {index}")
            harness = row.get("harness")
            if harness is not None:
                if not isinstance(harness, dict):
                    raise OrchestratorError(f"stored verification harness must be an object: {index}")
                harness_required = {"name", "revision", "doctor", "features", "artifacts"}
                harness_missing = sorted(harness_required - harness.keys())
                if harness_missing:
                    raise OrchestratorError(
                        f"stored verification harness {index} is missing fields: {', '.join(harness_missing)}"
                    )
                require_identifier(harness["name"], f"stored verification harness name {index}")
                require_text(harness["revision"], f"stored verification harness revision {index}")
                doctor = harness["doctor"]
                if not isinstance(doctor, str) or doctor not in DOCTOR_STATUSES:
                    raise OrchestratorError(f"stored verification doctor status is invalid: {index}")
                features = require_text_list(harness["features"], f"stored verification features {index}")
                artifacts = require_text_list(harness["artifacts"], f"stored verification artifacts {index}")
                if verdict == "verified" and (doctor != "passed" or not features or not artifacts):
                    raise OrchestratorError(
                        f"verified harness evidence requires a passed doctor, features, and artifacts: {index}"
                    )
            identity = (unit, revision)
            if identity in identities:
                raise OrchestratorError(f"stored verification is duplicated: {unit} {revision}")
            identities.add(identity)
        return value

    def gates(self) -> dict[str, dict[str, object]]:
        value = read_json(self.gates_path, {})
        if not isinstance(value, dict) or not all(isinstance(item, dict) for item in value.values()):
            raise OrchestratorError("gates.json must contain an object of gate objects")
        required = {"id", "status", "question", "default", "answer", "created_at", "resolved_at"}
        for identifier, gate in value.items():
            require_identifier(identifier, "stored gate key")
            missing = sorted(required - gate.keys())
            if missing:
                raise OrchestratorError(f"stored gate {identifier} is missing fields: {', '.join(missing)}")
            if require_identifier(gate["id"], "stored gate identifier") != identifier:
                raise OrchestratorError(f"stored gate identifier does not match its key: {identifier}")
            status = gate["status"]
            if not isinstance(status, str) or status not in {"open", "resolved"}:
                raise OrchestratorError(f"stored gate status is invalid: {identifier}")
            require_string(gate["question"], f"stored gate question for {identifier}")
            require_string(gate["default"], f"stored gate default for {identifier}")
            require_text(gate["created_at"], f"stored gate creation time for {identifier}")
            if status == "open":
                if gate["answer"] is not None or gate["resolved_at"] is not None:
                    raise OrchestratorError(f"open gate has resolution data: {identifier}")
            else:
                require_string(gate["answer"], f"stored gate answer for {identifier}")
                require_text(gate["resolved_at"], f"stored gate resolution time for {identifier}")
        return value

    def inbox_events_unlocked(self) -> list[dict[str, object]]:
        events: list[dict[str, object]] = []
        seen: set[str] = set()
        for queue, directory in (("pending", self.pending_inbox), ("processed", self.processed_inbox)):
            for path in sorted(directory.glob("*.json")):
                payload = read_json(path, {})
                if not isinstance(payload, dict):
                    raise OrchestratorError(f"inbox event must contain an object: {path}")
                required = {"event", "unit", "status", "report", "received_at"}
                missing = sorted(required - payload.keys())
                if missing:
                    raise OrchestratorError(f"inbox event {path.name} is missing fields: {', '.join(missing)}")
                event = require_identifier(payload["event"], f"stored inbox event in {path.name}")
                if path.name != f"{event}.json":
                    raise OrchestratorError(f"inbox event identifier does not match filename: {path.name}")
                if event in seen:
                    raise OrchestratorError(f"inbox event exists in multiple queues: {event}")
                seen.add(event)
                require_identifier(payload["unit"], f"stored inbox unit in {path.name}")
                require_text(payload["status"], f"stored inbox status in {path.name}")
                require_text(payload["report"], f"stored inbox report in {path.name}")
                require_text(payload["received_at"], f"stored inbox time in {path.name}")
                worker = payload.get("worker", "")
                thread = payload.get("thread", "")
                attempt = payload.get("attempt", 0)
                if worker == "" and thread == "" and attempt == 0:
                    pass
                elif isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
                    raise OrchestratorError(f"stored inbox attempt is invalid: {path.name}")
                else:
                    worker = require_text(worker, f"stored inbox worker in {path.name}")
                    thread = require_text(thread, f"stored inbox thread in {path.name}")
                events.append(
                    {
                        **payload,
                        "worker": worker,
                        "thread": thread,
                        "attempt": attempt,
                        "queue": queue,
                    }
                )
        return sorted(events, key=lambda row: (str(row.get("received_at", "")), str(row.get("event", ""))))

    def validate_store_unlocked(
        self,
    ) -> tuple[
        dict[str, object],
        dict[str, dict[str, object]],
        list[dict[str, object]],
        dict[str, dict[str, object]],
        list[dict[str, object]],
    ]:
        program = self.program()
        units = self.units()
        verification = self.verification()
        gates = self.gates()
        events = self.inbox_events_unlocked()
        for row in verification:
            if row["unit"] not in units:
                raise OrchestratorError(f"verification references unknown unit: {row['unit']}")
        for event in events:
            unit = units.get(str(event["unit"]))
            if unit is None:
                raise OrchestratorError(f"inbox event references unknown unit: {event['event']}")
            if event["attempt"]:
                attempt = next(
                    (
                        item
                        for item in unit["attempts"]
                        if item["attempt"] == event["attempt"]
                    ),
                    None,
                )
                if attempt is None:
                    raise OrchestratorError(f"inbox event references unknown attempt: {event['event']}")
                if event["worker"] != attempt["worker"] or event["thread"] != attempt["thread"]:
                    raise OrchestratorError(f"inbox event identity does not match attempt: {event['event']}")
        self.active_leases_unlocked(units)
        return program, units, verification, gates, events

    def init(self, goal: str, done: str, standing_orders: list[str]) -> dict[str, object]:
        goal = require_string(goal, "program goal")
        done = require_string(done, "done predicate")
        standing_orders = [require_string(order, "standing order") for order in standing_orders]
        with self.locked():
            self.pending_inbox.mkdir(parents=True, exist_ok=True)
            self.processed_inbox.mkdir(parents=True, exist_ok=True)
            if self.program_path.exists():
                existing = self.program()
                if existing.get("goal") != goal or existing.get("done_predicate") != done:
                    raise OrchestratorError("initialized program does not match the requested goal and predicate")
            else:
                write_json(
                    self.program_path,
                    {
                        "goal": goal,
                        "done_predicate": done,
                        "status": "active",
                        "created_at": now(),
                        "completed_at": None,
                    },
                )
            if not self.units_path.exists():
                write_json(self.units_path, {})
            if not self.verification_path.exists():
                write_json(self.verification_path, [])
            if not self.gates_path.exists():
                write_json(self.gates_path, {})
            state = self.validate_store_unlocked()
            requested_orders = "# Standing orders\n" + "".join(
                f"\n{index}. {order}\n" for index, order in enumerate(standing_orders, start=1)
            )
            if self.standing_orders_path.exists():
                if standing_orders and self.standing_orders_path.read_text(encoding="utf-8") != requested_orders:
                    raise OrchestratorError("existing standing orders differ from the requested values")
            else:
                atomic_write(self.standing_orders_path, requested_orders)
            snapshot = self.snapshot_from_state(*state)
            self.write_status_unlocked(snapshot)
            return snapshot

    def add_unit(
        self,
        identifier: str,
        goal: str,
        scope: str,
        acceptance: str,
        verify: str,
        dependencies: list[str],
    ) -> dict[str, object]:
        require_identifier(identifier, "unit identifier")
        goal = require_string(goal, "unit goal")
        scope = require_string(scope, "unit scope")
        acceptance = require_string(acceptance, "unit acceptance")
        verify = require_string(verify, "unit verification")
        dependencies = [require_identifier(value, "dependency") for value in dependencies]
        if identifier in dependencies:
            raise OrchestratorError("a unit cannot depend on itself")
        with self.locked():
            self.require_initialized()
            program, units, verification, gates, inbox_events = self.require_active()
            missing = sorted(value for value in dependencies if value not in units)
            if missing:
                raise OrchestratorError(f"unknown dependencies: {', '.join(missing)}")
            requested = {
                "id": identifier,
                "state": "pending",
                "revision": "",
                "assignment": None,
                "attempts": [],
                "goal": goal,
                "scope": scope,
                "acceptance": acceptance,
                "verify": verify,
                "depends_on": dependencies,
                "created_at": now(),
                "updated_at": now(),
            }
            existing = units.get(identifier)
            if existing is not None:
                stable_keys = ["id", "goal", "scope", "acceptance", "verify", "depends_on"]
                if {key: existing.get(key) for key in stable_keys} != {
                    key: requested[key] for key in stable_keys
                }:
                    raise OrchestratorError(f"unit already exists with different values: {identifier}")
                return existing
            units[identifier] = requested
            write_json(self.units_path, units)
            self.write_status_unlocked(
                self.snapshot_from_state(program, units, verification, gates, inbox_events)
            )
            return requested

    def active_leases_unlocked(self, units: dict[str, dict[str, object]]) -> list[dict[str, object]]:
        leases: list[dict[str, object]] = []
        for identifier in sorted(units):
            assignment = units[identifier].get("assignment")
            if not isinstance(assignment, dict):
                continue
            assigned_leases = assignment.get("leases")
            if not isinstance(assigned_leases, list) or not assigned_leases:
                raise OrchestratorError(f"active assignment has no scope leases: {identifier}")
            for value in assigned_leases:
                scope = canonicalize_lease(value)
                conflict = next(
                    (
                        row
                        for row in leases
                        if row.get("unit") != identifier
                        and leases_overlap(str(row.get("scope")), scope)
                    ),
                    None,
                )
                if conflict is not None:
                    raise OrchestratorError(f"scope lease has multiple active owners: {scope}")
                leases.append(
                    {
                        "scope": scope,
                        "unit": identifier,
                        "worker": assignment.get("worker", ""),
                        "thread": assignment.get("thread", ""),
                        "attempt": assignment.get("attempt", 0),
                    }
                )
        return leases

    def assign_unit(
        self,
        identifier: str,
        worker: str,
        thread: str,
        requested_leases: list[str],
    ) -> dict[str, object]:
        require_identifier(identifier, "unit identifier")
        worker = require_text(worker, "worker")
        thread = require_text(thread, "thread identity")
        with self.locked():
            self.require_initialized()
            program, units, verification, gates, inbox_events = self.require_active()
            unit = units.get(identifier)
            if unit is None:
                raise OrchestratorError(f"unknown unit: {identifier}")
            if unit.get("state") in TERMINAL_STATES or unit.get("state") == "verification":
                raise OrchestratorError(f"unit cannot be assigned from state: {unit.get('state')}")
            incomplete = [
                str(dependency)
                for dependency in unit.get("depends_on", [])
                if units.get(str(dependency), {}).get("state") != "done"
            ]
            if incomplete:
                raise OrchestratorError(f"incomplete dependencies: {', '.join(incomplete)}")
            if not requested_leases:
                raise OrchestratorError("assignment requires at least one canonical scope lease")
            leases = sorted({canonicalize_lease(value) for value in requested_leases})
            current = unit.get("assignment")
            if isinstance(current, dict):
                identity = {
                    "worker": current.get("worker"),
                    "thread": current.get("thread"),
                    "leases": current.get("leases"),
                }
                requested_identity = {"worker": worker, "thread": thread, "leases": leases}
                if identity == requested_identity:
                    return unit
                raise OrchestratorError(f"unit already has an active assignment: {identifier}")
            conflicts = [
                row
                for row in self.active_leases_unlocked(units)
                if row.get("unit") != identifier
                and any(leases_overlap(str(row.get("scope")), lease) for lease in leases)
            ]
            if conflicts:
                conflict = conflicts[0]
                raise OrchestratorError(
                    f"scope lease is owned by {conflict['unit']}: {conflict['scope']}"
                )
            attempts = unit.get("attempts", [])
            if not isinstance(attempts, list) or not all(isinstance(item, dict) for item in attempts):
                raise OrchestratorError(f"unit attempts must contain a list of objects: {identifier}")
            attempt_number = len(attempts) + 1
            timestamp = now()
            assignment = {
                "worker": worker,
                "thread": thread,
                "attempt": attempt_number,
                "leases": leases,
                "assigned_at": timestamp,
            }
            attempts.append(
                {
                    **assignment,
                    "started_at": timestamp,
                    "ended_at": None,
                    "outcome": None,
                }
            )
            unit["assignment"] = assignment
            unit["attempts"] = attempts
            unit["state"] = "running"
            unit["updated_at"] = timestamp
            write_json(self.units_path, units)
            self.write_status_unlocked(
                self.snapshot_from_state(program, units, verification, gates, inbox_events)
            )
            return unit

    def release_unit(
        self,
        identifier: str,
        outcome: str,
        revision: str | None,
        worker: str,
        thread: str,
        attempt: int,
    ) -> dict[str, object]:
        require_identifier(identifier, "unit identifier")
        worker = require_text(worker, "worker")
        thread = require_text(thread, "thread identity")
        if revision is not None:
            revision = require_text(revision, "revision or artifact identifier")
        if attempt < 1:
            raise OrchestratorError("attempt must be at least one")
        if outcome not in ATTEMPT_OUTCOMES:
            raise OrchestratorError(f"unknown attempt outcome: {outcome}")
        if outcome == "completed" and not revision:
            raise OrchestratorError("a completed attempt requires a revision or artifact identifier")
        with self.locked():
            self.require_initialized()
            program, units, verification, gates, inbox_events = self.require_active()
            unit = units.get(identifier)
            if unit is None:
                raise OrchestratorError(f"unknown unit: {identifier}")
            attempts = unit.get("attempts", [])
            if not isinstance(attempts, list) or not all(isinstance(item, dict) for item in attempts):
                raise OrchestratorError(f"unit attempts must contain a list of objects: {identifier}")
            assignment = unit.get("assignment")
            if not isinstance(assignment, dict):
                previous = next(
                    (item for item in reversed(attempts) if item.get("attempt") == attempt),
                    None,
                )
                if (
                    previous is not None
                    and previous.get("worker") == worker
                    and previous.get("thread") == thread
                    and previous.get("outcome") == outcome
                    and (revision is None or unit.get("revision") == revision)
                ):
                    return unit
                raise OrchestratorError(f"unit has no active assignment: {identifier}")
            expected_identity = {"worker": worker, "thread": thread, "attempt": attempt}
            current_identity = {key: assignment.get(key) for key in expected_identity}
            if current_identity != expected_identity:
                raise OrchestratorError(f"release identity does not match active assignment: {identifier}")
            current_attempt = next(
                (item for item in reversed(attempts) if item.get("attempt") == attempt),
                None,
            )
            if current_attempt is None:
                raise OrchestratorError(f"active assignment has no matching attempt: {identifier}")
            timestamp = now()
            current_attempt["ended_at"] = timestamp
            current_attempt["outcome"] = outcome
            unit["assignment"] = None
            unit["attempts"] = attempts
            if revision is not None:
                unit["revision"] = revision
            unit["state"] = {
                "completed": "verification",
                "blocked": "blocked",
                "failed": "blocked",
                "cancelled": "pending",
            }[outcome]
            unit["updated_at"] = timestamp
            write_json(self.units_path, units)
            self.write_status_unlocked(
                self.snapshot_from_state(program, units, verification, gates, inbox_events)
            )
            return unit

    def set_unit(self, identifier: str, state: str, revision: str | None) -> dict[str, object]:
        require_identifier(identifier, "unit identifier")
        if revision is not None:
            revision = require_text(revision, "revision or artifact identifier")
        if state not in UNIT_STATES:
            raise OrchestratorError(f"unknown unit state: {state}")
        with self.locked():
            self.require_initialized()
            program, units, verification, gates, inbox_events = self.require_active()
            unit = units.get(identifier)
            if unit is None:
                raise OrchestratorError(f"unknown unit: {identifier}")
            if isinstance(unit.get("assignment"), dict) and state != "running":
                raise OrchestratorError("release the active assignment before changing unit state")
            if state == "done":
                incomplete = [
                    str(dependency)
                    for dependency in unit.get("depends_on", [])
                    if units.get(str(dependency), {}).get("state") != "done"
                ]
                if incomplete:
                    raise OrchestratorError(f"incomplete dependencies: {', '.join(incomplete)}")
            if revision is not None:
                unit["revision"] = revision
            if state == "done":
                stored_revision = unit.get("revision")
                if not isinstance(stored_revision, str):
                    raise OrchestratorError("a done unit requires a revision or artifact identifier")
                require_text(stored_revision, "revision or artifact identifier")
            if state == "done":
                verdict = self.verification_for(unit, verification)
                if verdict["verdict"] != "verified":
                    raise OrchestratorError("a done unit requires current verified evidence")
            unit["state"] = state
            unit["updated_at"] = now()
            write_json(self.units_path, units)
            self.write_status_unlocked(
                self.snapshot_from_state(program, units, verification, gates, inbox_events)
            )
            return unit

    def push_inbox(
        self,
        event: str,
        unit: str,
        status: str,
        report: str,
        worker: str | None,
        thread: str | None,
        attempt: int | None,
    ) -> dict[str, object]:
        require_identifier(event, "event identifier")
        require_identifier(unit, "unit identifier")
        status = require_text(status, "inbox status")
        report = require_text(report, "inbox report")
        with self.locked():
            self.require_initialized()
            _, units, _, _, _ = self.require_active()
            unit_record = units.get(unit)
            if unit_record is None:
                raise OrchestratorError(f"unknown unit: {unit}")
            requested = {
                "event": event,
                "unit": unit,
                "status": status,
                "report": report,
                "worker": worker or "",
                "thread": thread or "",
                "attempt": attempt or 0,
            }
            for directory in (self.pending_inbox, self.processed_inbox):
                path = directory / f"{event}.json"
                if path.exists():
                    existing = read_json(path, {})
                    if not isinstance(existing, dict):
                        raise OrchestratorError(f"inbox event must contain an object: {path}")
                    comparable = {
                        "event": existing.get("event"),
                        "unit": existing.get("unit"),
                        "status": existing.get("status"),
                        "report": existing.get("report"),
                        "worker": existing.get("worker", ""),
                        "thread": existing.get("thread", ""),
                        "attempt": existing.get("attempt", 0),
                    }
                    if comparable != requested:
                        raise OrchestratorError(f"inbox event already exists with different values: {event}")
                    return {**existing, "duplicate": True}
            attempts = unit_record.get("attempts", [])
            if not isinstance(attempts, list) or not all(isinstance(item, dict) for item in attempts):
                raise OrchestratorError(f"unit attempts must contain a list of objects: {unit}")
            if attempts:
                if attempt is None or worker is None or thread is None:
                    raise OrchestratorError("inbox event for an assigned unit requires worker, thread, and attempt")
                identity = next(
                    (item for item in reversed(attempts) if item.get("attempt") == attempt),
                    None,
                )
                if identity is None:
                    raise OrchestratorError(f"unknown unit attempt: {unit} attempt {attempt}")
                if worker != identity.get("worker") or thread != identity.get("thread"):
                    raise OrchestratorError(f"inbox identity does not match unit attempt: {unit}")
            elif attempt is not None or worker is not None or thread is not None:
                raise OrchestratorError("inbox identity requires a stored unit attempt")
            payload = {**requested, "received_at": now()}
            write_json(self.pending_inbox / f"{event}.json", payload)
            return {**payload, "duplicate": False}

    def drain_inbox(self) -> list[dict[str, object]]:
        with self.locked():
            self.require_initialized()
            self.require_active()
            drained: list[dict[str, object]] = []
            for path in sorted(self.pending_inbox.glob("*.json")):
                payload = read_json(path, {})
                if not isinstance(payload, dict):
                    raise OrchestratorError(f"inbox event must contain an object: {path}")
                os.replace(path, self.processed_inbox / path.name)
                drained.append(payload)
            return drained

    def record_verification(
        self,
        unit_id: str,
        revision: str,
        verdict: str,
        evidence: str,
        harness_name: str | None = None,
        harness_revision: str | None = None,
        doctor: str | None = None,
        features: list[str] | None = None,
        artifacts: list[str] | None = None,
    ) -> dict[str, object]:
        require_identifier(unit_id, "unit identifier")
        revision = require_text(revision, "revision or artifact identifier")
        evidence = require_string(evidence, "verification evidence")
        if verdict not in VERDICTS:
            raise OrchestratorError(f"unknown verification verdict: {verdict}")
        features = require_text_list(features or [], "verification features")
        artifacts = require_text_list(artifacts or [], "verification artifacts")
        harness_requested = any(
            value is not None and value != []
            for value in (harness_name, harness_revision, doctor, features, artifacts)
        )
        harness: dict[str, object] | None = None
        if harness_requested:
            if harness_name is None or harness_revision is None or doctor is None:
                raise OrchestratorError(
                    "structured harness evidence requires --harness, --harness-revision, and --doctor"
                )
            harness_name = require_identifier(harness_name, "verification harness name")
            harness_revision = require_text(harness_revision, "verification harness revision")
            if doctor not in DOCTOR_STATUSES:
                raise OrchestratorError(f"unknown doctor status: {doctor}")
            if verdict == "verified" and (doctor != "passed" or not features or not artifacts):
                raise OrchestratorError(
                    "verified harness evidence requires --doctor passed, at least one --feature, and at least one --artifact"
                )
            harness = {
                "name": harness_name,
                "revision": harness_revision,
                "doctor": doctor,
                "features": features,
                "artifacts": artifacts,
            }
        with self.locked():
            self.require_initialized()
            program, units, rows, gates, inbox_events = self.require_active()
            unit = units.get(unit_id)
            if unit is None:
                raise OrchestratorError(f"unknown unit: {unit_id}")
            if unit.get("revision") != revision:
                raise OrchestratorError(f"verification revision does not match current unit revision: {unit_id}")
            entry = {
                "unit": unit_id,
                "revision": revision,
                "verdict": verdict,
                "evidence": evidence,
                "recorded_at": now(),
            }
            if harness is not None:
                entry["harness"] = harness
            rows = [
                row
                for row in rows
                if row.get("unit") != unit_id or row.get("revision") != revision
            ]
            rows.append(entry)
            write_json(self.verification_path, rows)
            self.write_status_unlocked(
                self.snapshot_from_state(program, units, rows, gates, inbox_events)
            )
            return entry

    def check_verification(self, unit_id: str) -> dict[str, object]:
        require_identifier(unit_id, "unit identifier")
        with self.locked():
            self.require_initialized()
            _, units, verification, _, _ = self.validate_store_unlocked()
            unit = units.get(unit_id)
            if unit is None:
                raise OrchestratorError(f"unknown unit: {unit_id}")
            result = self.verification_for(unit, verification)
            if result["verdict"] != "verified":
                raise OrchestratorError(
                    f"unit does not have current verified evidence: {unit_id} ({result['verdict']})"
                )
            return result

    def add_gate(self, identifier: str, question: str, default: str) -> dict[str, object]:
        require_identifier(identifier, "gate identifier")
        question = require_string(question, "gate question")
        default = require_string(default, "gate default")
        with self.locked():
            self.require_initialized()
            program, units, verification, gates, inbox_events = self.require_active()
            requested = {
                "id": identifier,
                "status": "open",
                "question": question,
                "default": default,
                "answer": None,
                "created_at": now(),
                "resolved_at": None,
            }
            existing = gates.get(identifier)
            if existing is not None:
                stable_keys = ("id", "status", "question", "default", "answer")
                if {key: existing.get(key) for key in stable_keys} != {
                    key: requested[key] for key in stable_keys
                }:
                    raise OrchestratorError(f"gate already exists with different values: {identifier}")
                return existing
            gates[identifier] = requested
            write_json(self.gates_path, gates)
            self.write_status_unlocked(
                self.snapshot_from_state(program, units, verification, gates, inbox_events)
            )
            return requested

    def resolve_gate(self, identifier: str, answer: str) -> dict[str, object]:
        require_identifier(identifier, "gate identifier")
        answer = require_string(answer, "gate answer")
        with self.locked():
            self.require_initialized()
            program, units, verification, gates, inbox_events = self.require_active()
            gate = gates.get(identifier)
            if gate is None:
                raise OrchestratorError(f"unknown gate: {identifier}")
            gate["status"] = "resolved"
            gate["answer"] = answer
            gate["resolved_at"] = now()
            write_json(self.gates_path, gates)
            self.write_status_unlocked(
                self.snapshot_from_state(program, units, verification, gates, inbox_events)
            )
            return gate

    def verification_for(
        self,
        unit: dict[str, object],
        rows: list[dict[str, object]],
    ) -> dict[str, object]:
        revision = unit.get("revision")
        if not isinstance(revision, str) or not revision.strip():
            return {
                "unit": unit.get("id"),
                "revision": revision,
                "verdict": "missing",
                "evidence": "",
            }
        unit_rows = [row for row in rows if row.get("unit") == unit.get("id")]
        current = [row for row in unit_rows if row.get("revision") == revision]
        if current:
            return current[-1]
        return {
            "unit": unit.get("id"),
            "revision": revision,
            "verdict": "stale" if unit_rows else "missing",
            "evidence": "",
        }

    def snapshot_unlocked(self) -> dict[str, object]:
        self.require_initialized()
        return self.snapshot_from_state(*self.validate_store_unlocked())

    def snapshot_from_state(
        self,
        program: dict[str, object],
        units: dict[str, dict[str, object]],
        verification: list[dict[str, object]],
        gates: dict[str, dict[str, object]],
        inbox_events: list[dict[str, object]],
    ) -> dict[str, object]:
        latest_reports: dict[str, dict[str, object]] = {}
        for event in inbox_events:
            unit_id = str(event.get("unit", ""))
            if unit_id:
                latest_reports[unit_id] = event
        unit_rows: list[dict[str, object]] = []
        for identifier in sorted(units):
            unit = units[identifier]
            dependencies = [str(value) for value in unit.get("depends_on", [])]
            ready = unit.get("state") == "pending" and all(
                units.get(dependency, {}).get("state") == "done" for dependency in dependencies
            )
            verdict = self.verification_for(unit, verification)
            unit_rows.append(
                {
                    **unit,
                    "ready": ready,
                    "verification": verdict["verdict"],
                    "latest_report": latest_reports.get(identifier),
                }
            )
        open_gates = [gate for gate in gates.values() if gate.get("status") == "open"]
        all_terminal = bool(unit_rows) and all(row.get("state") in TERMINAL_STATES for row in unit_rows)
        all_done_verified = all(
            row.get("state") != "done" or row.get("verification") == "verified" for row in unit_rows
        )
        counts = Counter(str(row.get("state")) for row in unit_rows)
        pending_inbox_count = sum(event.get("queue") == "pending" for event in inbox_events)
        active_leases = self.active_leases_unlocked(units)
        active_assignment_count = sum(isinstance(unit.get("assignment"), dict) for unit in units.values())
        return {
            "program": program,
            "unit_count": len(unit_rows),
            "counts": dict(sorted(counts.items())),
            "ready": [row["id"] for row in unit_rows if row["ready"]],
            "units": unit_rows,
            "open_gates": sorted(str(gate.get("id")) for gate in open_gates),
            "pending_inbox_count": pending_inbox_count,
            "active_leases": active_leases,
            "active_assignment_count": active_assignment_count,
            "can_close": (
                all_terminal
                and all_done_verified
                and not open_gates
                and pending_inbox_count == 0
                and not active_leases
                and active_assignment_count == 0
            ),
        }

    def snapshot(self) -> dict[str, object]:
        with self.locked():
            snapshot = self.snapshot_unlocked()
            self.write_status_unlocked(snapshot)
            return snapshot

    def write_status_unlocked(self, snapshot: dict[str, object]) -> None:
        program = snapshot["program"]
        units = snapshot["units"]
        lines = [
            "# Orchestration status",
            "",
            f"Goal: {program['goal']}",
            f"Done predicate: {program['done_predicate']}",
            f"Program status: {program['status']}",
            f"Can close: {'yes' if snapshot['can_close'] else 'no'}",
            f"Pending inbox events: {snapshot['pending_inbox_count']}",
            f"Active assignments: {snapshot['active_assignment_count']}",
            "",
            "## Units",
            "",
            "| Unit | State | Attempt | Worker | Thread | Leases | Revision | Verification | Ready |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for unit in units:
            assignment = unit.get("assignment") if isinstance(unit.get("assignment"), dict) else {}
            attempts = unit.get("attempts") if isinstance(unit.get("attempts"), list) else []
            leases = ", ".join(str(value) for value in assignment.get("leases", []))
            lines.append(
                f"| {markdown_cell(unit['id'])} | {markdown_cell(unit['state'])} | {len(attempts) or '-'} | "
                f"{markdown_cell(assignment.get('worker') or '-')} | "
                f"{markdown_cell(assignment.get('thread') or '-')} | {markdown_cell(leases or '-')} | "
                f"{markdown_cell(unit['revision'] or '-')} | {markdown_cell(unit['verification'])} | "
                f"{'yes' if unit['ready'] else 'no'} |"
            )
        lines.extend(
            [
                "",
                "## Latest reports",
                "",
                "| Unit | Queue | Attempt | Worker | Thread | Status | Report |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        reports = [
            (unit["id"], unit.get("latest_report"))
            for unit in units
            if isinstance(unit.get("latest_report"), dict)
        ]
        for unit_id, report in reports:
            lines.append(
                f"| {markdown_cell(unit_id)} | {markdown_cell(report.get('queue') or '-')} | "
                f"{markdown_cell(report.get('attempt') or '-')} | "
                f"{markdown_cell(report.get('worker') or '-')} | "
                f"{markdown_cell(report.get('thread') or '-')} | "
                f"{markdown_cell(report.get('status') or '-')} | "
                f"{markdown_cell(report.get('report') or '-')} |"
            )
        if not reports:
            lines.append("| - | - | - | - | - | - | - |")
        lines.extend(["", "## Open gates", ""])
        open_gates = snapshot["open_gates"]
        lines.extend(f"1. {identifier}" for identifier in open_gates)
        if not open_gates:
            lines.append("None.")
        atomic_write(self.status_path, "\n".join(lines) + "\n")

    def close(self) -> dict[str, object]:
        with self.locked():
            self.require_initialized()
            program, units, verification, gates, inbox_events = self.validate_store_unlocked()
            snapshot = self.snapshot_from_state(program, units, verification, gates, inbox_events)
            if program.get("status") == "complete":
                closed = snapshot
                self.write_status_unlocked(closed)
                return closed
            if not snapshot["can_close"]:
                raise OrchestratorError("program cannot close until all units and gates satisfy the predicate")
            program["status"] = "complete"
            program["completed_at"] = now()
            write_json(self.program_path, program)
            closed = self.snapshot_from_state(program, units, verification, gates, inbox_events)
            self.write_status_unlocked(closed)
            return closed


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Durable local orchestration state")
    root.add_argument("--store", type=Path, required=True)
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init")
    init.add_argument("--goal", required=True)
    init.add_argument("--done", required=True)
    init.add_argument("--standing-order", action="append", default=[])

    unit = commands.add_parser("unit")
    unit_commands = unit.add_subparsers(dest="unit_command", required=True)
    unit_add = unit_commands.add_parser("add")
    unit_add.add_argument("id")
    unit_add.add_argument("--goal", required=True)
    unit_add.add_argument("--scope", required=True)
    unit_add.add_argument("--acceptance", required=True)
    unit_add.add_argument("--verify", required=True)
    unit_add.add_argument("--depends-on", action="append", default=[])
    unit_set = unit_commands.add_parser("set")
    unit_set.add_argument("id")
    unit_set.add_argument("--state", required=True)
    unit_set.add_argument("--revision")
    unit_assign = unit_commands.add_parser("assign")
    unit_assign.add_argument("id")
    unit_assign.add_argument("--worker", required=True)
    unit_assign.add_argument("--thread", required=True)
    unit_assign.add_argument("--lease", action="append", default=[])
    unit_release = unit_commands.add_parser("release")
    unit_release.add_argument("id")
    unit_release.add_argument("--outcome", required=True)
    unit_release.add_argument("--revision")
    unit_release.add_argument("--worker", required=True)
    unit_release.add_argument("--thread", required=True)
    unit_release.add_argument("--attempt", required=True, type=int)

    inbox = commands.add_parser("inbox")
    inbox_commands = inbox.add_subparsers(dest="inbox_command", required=True)
    inbox_push = inbox_commands.add_parser("push")
    inbox_push.add_argument("event")
    inbox_push.add_argument("--unit", required=True)
    inbox_push.add_argument("--status", required=True)
    inbox_push.add_argument("--report", required=True)
    inbox_push.add_argument("--worker")
    inbox_push.add_argument("--thread")
    inbox_push.add_argument("--attempt", type=int)
    inbox_commands.add_parser("drain")

    verification = commands.add_parser("verification")
    verification_commands = verification.add_subparsers(dest="verification_command", required=True)
    verification_record = verification_commands.add_parser("record")
    verification_record.add_argument("unit")
    verification_record.add_argument("--revision", required=True)
    verification_record.add_argument("--verdict", required=True)
    verification_record.add_argument("--evidence", required=True)
    verification_record.add_argument("--harness")
    verification_record.add_argument("--harness-revision")
    verification_record.add_argument("--doctor", choices=sorted(DOCTOR_STATUSES))
    verification_record.add_argument("--feature", action="append", default=[])
    verification_record.add_argument("--artifact", action="append", default=[])
    verification_check = verification_commands.add_parser("check")
    verification_check.add_argument("unit")

    gate = commands.add_parser("gate")
    gate_commands = gate.add_subparsers(dest="gate_command", required=True)
    gate_add = gate_commands.add_parser("add")
    gate_add.add_argument("id")
    gate_add.add_argument("--question", required=True)
    gate_add.add_argument("--default", required=True)
    gate_resolve = gate_commands.add_parser("resolve")
    gate_resolve.add_argument("id")
    gate_resolve.add_argument("--answer", required=True)

    commands.add_parser("status")
    commands.add_parser("resume")
    commands.add_parser("close")
    return root


def execute(arguments: argparse.Namespace) -> object:
    store = Store(arguments.store)
    if arguments.command == "init":
        return store.init(arguments.goal, arguments.done, arguments.standing_order)
    if arguments.command == "unit" and arguments.unit_command == "add":
        return store.add_unit(
            arguments.id,
            arguments.goal,
            arguments.scope,
            arguments.acceptance,
            arguments.verify,
            arguments.depends_on,
        )
    if arguments.command == "unit" and arguments.unit_command == "set":
        return store.set_unit(arguments.id, arguments.state, arguments.revision)
    if arguments.command == "unit" and arguments.unit_command == "assign":
        return store.assign_unit(arguments.id, arguments.worker, arguments.thread, arguments.lease)
    if arguments.command == "unit" and arguments.unit_command == "release":
        return store.release_unit(
            arguments.id,
            arguments.outcome,
            arguments.revision,
            arguments.worker,
            arguments.thread,
            arguments.attempt,
        )
    if arguments.command == "inbox" and arguments.inbox_command == "push":
        return store.push_inbox(
            arguments.event,
            arguments.unit,
            arguments.status,
            arguments.report,
            arguments.worker,
            arguments.thread,
            arguments.attempt,
        )
    if arguments.command == "inbox" and arguments.inbox_command == "drain":
        return store.drain_inbox()
    if arguments.command == "verification" and arguments.verification_command == "record":
        return store.record_verification(
            arguments.unit,
            arguments.revision,
            arguments.verdict,
            arguments.evidence,
            arguments.harness,
            arguments.harness_revision,
            arguments.doctor,
            arguments.feature,
            arguments.artifact,
        )
    if arguments.command == "verification" and arguments.verification_command == "check":
        return store.check_verification(arguments.unit)
    if arguments.command == "gate" and arguments.gate_command == "add":
        return store.add_gate(arguments.id, arguments.question, arguments.default)
    if arguments.command == "gate" and arguments.gate_command == "resolve":
        return store.resolve_gate(arguments.id, arguments.answer)
    if arguments.command in {"status", "resume"}:
        return store.snapshot()
    if arguments.command == "close":
        return store.close()
    raise OrchestratorError("unsupported command")


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        result = execute(arguments)
    except OrchestratorError as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
