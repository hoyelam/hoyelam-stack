#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import sys
import tempfile
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


UNIT_STATES = {"pending", "running", "verification", "blocked", "done", "abandoned"}
TERMINAL_STATES = {"done", "abandoned"}
VERDICTS = {"verified", "failed", "blocked"}
SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


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


def atomic_write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
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


def require_identifier(value: str, label: str) -> str:
    if not SAFE_IDENTIFIER.fullmatch(value):
        raise OrchestratorError(f"{label} must match {SAFE_IDENTIFIER.pattern}")
    return value


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
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def require_initialized(self) -> None:
        if not self.program_path.is_file():
            raise OrchestratorError(f"store is not initialized: {self.root}")

    def require_active(self) -> None:
        if self.program().get("status") != "active":
            raise OrchestratorError("program is closed and cannot be mutated")

    def program(self) -> dict[str, object]:
        value = read_json(self.program_path, {})
        if not isinstance(value, dict):
            raise OrchestratorError("program.json must contain an object")
        return value

    def units(self) -> dict[str, dict[str, object]]:
        value = read_json(self.units_path, {})
        if not isinstance(value, dict) or not all(isinstance(item, dict) for item in value.values()):
            raise OrchestratorError("units.json must contain an object of unit objects")
        return value

    def verification(self) -> list[dict[str, object]]:
        value = read_json(self.verification_path, [])
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            raise OrchestratorError("verification.json must contain a list")
        return value

    def gates(self) -> dict[str, dict[str, object]]:
        value = read_json(self.gates_path, {})
        if not isinstance(value, dict) or not all(isinstance(item, dict) for item in value.values()):
            raise OrchestratorError("gates.json must contain an object of gate objects")
        return value

    def init(self, goal: str, done: str, standing_orders: list[str]) -> dict[str, object]:
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
            requested_orders = "# Standing orders\n" + "".join(
                f"\n{index}. {order}\n" for index, order in enumerate(standing_orders, start=1)
            )
            if self.standing_orders_path.exists():
                if standing_orders and self.standing_orders_path.read_text(encoding="utf-8") != requested_orders:
                    raise OrchestratorError("existing standing orders differ from the requested values")
            else:
                atomic_write(self.standing_orders_path, requested_orders)
            snapshot = self.snapshot_unlocked()
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
        dependencies = [require_identifier(value, "dependency") for value in dependencies]
        if identifier in dependencies:
            raise OrchestratorError("a unit cannot depend on itself")
        with self.locked():
            self.require_initialized()
            self.require_active()
            units = self.units()
            missing = sorted(value for value in dependencies if value not in units)
            if missing:
                raise OrchestratorError(f"unknown dependencies: {', '.join(missing)}")
            requested = {
                "id": identifier,
                "state": "pending",
                "revision": "",
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
                stable_keys = [key for key in requested if key not in {"created_at", "updated_at"}]
                if {key: existing.get(key) for key in stable_keys} != {
                    key: requested[key] for key in stable_keys
                }:
                    raise OrchestratorError(f"unit already exists with different values: {identifier}")
                return existing
            units[identifier] = requested
            write_json(self.units_path, units)
            self.write_status_unlocked(self.snapshot_unlocked())
            return requested

    def set_unit(self, identifier: str, state: str, revision: str | None) -> dict[str, object]:
        require_identifier(identifier, "unit identifier")
        if state not in UNIT_STATES:
            raise OrchestratorError(f"unknown unit state: {state}")
        with self.locked():
            self.require_initialized()
            self.require_active()
            units = self.units()
            unit = units.get(identifier)
            if unit is None:
                raise OrchestratorError(f"unknown unit: {identifier}")
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
            if state == "done" and not unit.get("revision"):
                raise OrchestratorError("a done unit requires a revision or artifact identifier")
            if state == "done":
                verdict = self.verification_for(unit, self.verification())
                if verdict["verdict"] != "verified":
                    raise OrchestratorError("a done unit requires current verified evidence")
            unit["state"] = state
            unit["updated_at"] = now()
            write_json(self.units_path, units)
            self.write_status_unlocked(self.snapshot_unlocked())
            return unit

    def push_inbox(self, event: str, unit: str, status: str, report: str) -> dict[str, object]:
        require_identifier(event, "event identifier")
        require_identifier(unit, "unit identifier")
        with self.locked():
            self.require_initialized()
            self.require_active()
            if unit not in self.units():
                raise OrchestratorError(f"unknown unit: {unit}")
            expected = {"event": event, "unit": unit, "status": status, "report": report}
            for directory in (self.pending_inbox, self.processed_inbox):
                path = directory / f"{event}.json"
                if path.exists():
                    existing = read_json(path, {})
                    comparable = {key: existing.get(key) for key in expected} if isinstance(existing, dict) else {}
                    if comparable != expected:
                        raise OrchestratorError(f"inbox event already exists with different values: {event}")
                    return {**existing, "duplicate": True}
            payload = {**expected, "received_at": now()}
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
    ) -> dict[str, object]:
        require_identifier(unit_id, "unit identifier")
        if verdict not in VERDICTS:
            raise OrchestratorError(f"unknown verification verdict: {verdict}")
        if not revision:
            raise OrchestratorError("verification requires a revision or artifact identifier")
        with self.locked():
            self.require_initialized()
            self.require_active()
            units = self.units()
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
            rows = [
                row
                for row in self.verification()
                if row.get("unit") != unit_id or row.get("revision") != revision
            ]
            rows.append(entry)
            write_json(self.verification_path, rows)
            self.write_status_unlocked(self.snapshot_unlocked())
            return entry

    def check_verification(self, unit_id: str) -> dict[str, object]:
        require_identifier(unit_id, "unit identifier")
        with self.locked():
            self.require_initialized()
            unit = self.units().get(unit_id)
            if unit is None:
                raise OrchestratorError(f"unknown unit: {unit_id}")
            result = self.verification_for(unit, self.verification())
            if result["verdict"] != "verified":
                raise OrchestratorError(
                    f"unit does not have current verified evidence: {unit_id} ({result['verdict']})"
                )
            return result

    def add_gate(self, identifier: str, question: str, default: str) -> dict[str, object]:
        require_identifier(identifier, "gate identifier")
        with self.locked():
            self.require_initialized()
            self.require_active()
            gates = self.gates()
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
            self.write_status_unlocked(self.snapshot_unlocked())
            return requested

    def resolve_gate(self, identifier: str, answer: str) -> dict[str, object]:
        require_identifier(identifier, "gate identifier")
        with self.locked():
            self.require_initialized()
            self.require_active()
            gates = self.gates()
            gate = gates.get(identifier)
            if gate is None:
                raise OrchestratorError(f"unknown gate: {identifier}")
            gate["status"] = "resolved"
            gate["answer"] = answer
            gate["resolved_at"] = now()
            write_json(self.gates_path, gates)
            self.write_status_unlocked(self.snapshot_unlocked())
            return gate

    def verification_for(
        self,
        unit: dict[str, object],
        rows: list[dict[str, object]],
    ) -> dict[str, object]:
        unit_rows = [row for row in rows if row.get("unit") == unit.get("id")]
        current = [row for row in unit_rows if row.get("revision") == unit.get("revision")]
        if current:
            return current[-1]
        return {
            "unit": unit.get("id"),
            "revision": unit.get("revision"),
            "verdict": "stale" if unit_rows else "missing",
            "evidence": "",
        }

    def snapshot_unlocked(self) -> dict[str, object]:
        self.require_initialized()
        program = self.program()
        units = self.units()
        verification = self.verification()
        gates = self.gates()
        unit_rows: list[dict[str, object]] = []
        for identifier in sorted(units):
            unit = units[identifier]
            dependencies = [str(value) for value in unit.get("depends_on", [])]
            ready = unit.get("state") == "pending" and all(
                units.get(dependency, {}).get("state") == "done" for dependency in dependencies
            )
            verdict = self.verification_for(unit, verification)
            unit_rows.append({**unit, "ready": ready, "verification": verdict["verdict"]})
        open_gates = [gate for gate in gates.values() if gate.get("status") == "open"]
        all_terminal = bool(unit_rows) and all(row.get("state") in TERMINAL_STATES for row in unit_rows)
        all_done_verified = all(
            row.get("state") != "done" or row.get("verification") == "verified" for row in unit_rows
        )
        counts = Counter(str(row.get("state")) for row in unit_rows)
        pending_inbox_count = len(list(self.pending_inbox.glob("*.json")))
        return {
            "program": program,
            "unit_count": len(unit_rows),
            "counts": dict(sorted(counts.items())),
            "ready": [row["id"] for row in unit_rows if row["ready"]],
            "units": unit_rows,
            "open_gates": sorted(str(gate.get("id")) for gate in open_gates),
            "pending_inbox_count": pending_inbox_count,
            "can_close": all_terminal and all_done_verified and not open_gates and pending_inbox_count == 0,
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
            "",
            "## Units",
            "",
            "| Unit | State | Revision | Verification | Ready |",
            "| --- | --- | --- | --- | --- |",
        ]
        for unit in units:
            lines.append(
                f"| {unit['id']} | {unit['state']} | {unit['revision'] or '-'} | "
                f"{unit['verification']} | {'yes' if unit['ready'] else 'no'} |"
            )
        lines.extend(["", "## Open gates", ""])
        open_gates = snapshot["open_gates"]
        lines.extend(f"1. {identifier}" for identifier in open_gates)
        if not open_gates:
            lines.append("None.")
        atomic_write(self.status_path, "\n".join(lines) + "\n")

    def close(self) -> dict[str, object]:
        with self.locked():
            self.require_initialized()
            if self.program().get("status") == "complete":
                closed = self.snapshot_unlocked()
                self.write_status_unlocked(closed)
                return closed
            snapshot = self.snapshot_unlocked()
            if not snapshot["can_close"]:
                raise OrchestratorError("program cannot close until all units and gates satisfy the predicate")
            program = self.program()
            program["status"] = "complete"
            program["completed_at"] = now()
            write_json(self.program_path, program)
            closed = self.snapshot_unlocked()
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

    inbox = commands.add_parser("inbox")
    inbox_commands = inbox.add_subparsers(dest="inbox_command", required=True)
    inbox_push = inbox_commands.add_parser("push")
    inbox_push.add_argument("event")
    inbox_push.add_argument("--unit", required=True)
    inbox_push.add_argument("--status", required=True)
    inbox_push.add_argument("--report", required=True)
    inbox_commands.add_parser("drain")

    verification = commands.add_parser("verification")
    verification_commands = verification.add_subparsers(dest="verification_command", required=True)
    verification_record = verification_commands.add_parser("record")
    verification_record.add_argument("unit")
    verification_record.add_argument("--revision", required=True)
    verification_record.add_argument("--verdict", required=True)
    verification_record.add_argument("--evidence", required=True)
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
    if arguments.command == "inbox" and arguments.inbox_command == "push":
        return store.push_inbox(arguments.event, arguments.unit, arguments.status, arguments.report)
    if arguments.command == "inbox" and arguments.inbox_command == "drain":
        return store.drain_inbox()
    if arguments.command == "verification" and arguments.verification_command == "record":
        return store.record_verification(
            arguments.unit,
            arguments.revision,
            arguments.verdict,
            arguments.evidence,
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
