#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
from typing import Any


def compact(value: str, limit: int = 2000) -> str:
    value = value.strip()
    return value if len(value) <= limit else f"{value[:limit]}\n… truncated"


def run(command: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20, check=False)
        return {
            "available": True,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": compact(result.stderr),
        }
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"available": False, "error": str(error)}


def find_simulator(devices: dict[str, Any], simulator_id: str) -> dict[str, Any] | None:
    for runtime, runtime_devices in devices.get("devices", {}).items():
        for device in runtime_devices:
            if device.get("udid") == simulator_id:
                return {"runtime": runtime, **device}
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", choices=("ios", "macos"), required=True)
    parser.add_argument("--simulator-id")
    parser.add_argument("--bundle-id")
    parser.add_argument("--process-name")
    arguments = parser.parse_args()

    tools = {name: shutil.which(name) for name in ("xcodebuild", "xcrun", "maestro")}
    xcode = run([tools["xcodebuild"], "-version"]) if tools["xcodebuild"] else None
    maestro = run([tools["maestro"], "--version"]) if tools["maestro"] else None
    report: dict[str, Any] = {
        "host": platform.system(),
        "platform": arguments.platform,
        "tools": tools,
        "xcode": xcode,
        "maestro": maestro,
    }

    ready = (
        report["host"] == "Darwin"
        and tools["xcodebuild"] is not None
        and xcode is not None
        and xcode.get("exit_code") == 0
    )

    if arguments.platform == "ios":
        ready = ready and tools["xcrun"] is not None
        simulator_report: dict[str, Any] | None = None
        if tools["xcrun"]:
            devices_result = run([tools["xcrun"], "simctl", "list", "devices", "available", "-j"])
            ready = ready and devices_result.get("exit_code") == 0
            simulator_report = {
                "query": {key: value for key, value in devices_result.items() if key != "stdout"}
            }
            if devices_result.get("exit_code") == 0:
                try:
                    devices = json.loads(devices_result.get("stdout", "{}"))
                except json.JSONDecodeError as error:
                    simulator_report["parse_error"] = str(error)
                    ready = False
                else:
                    available = [
                        {
                            "runtime": runtime,
                            "name": device.get("name"),
                            "udid": device.get("udid"),
                            "state": device.get("state"),
                        }
                        for runtime, runtime_devices in devices.get("devices", {}).items()
                        for device in runtime_devices
                    ]
                    simulator_report["available_count"] = len(available)
                    simulator_report["booted"] = [device for device in available if device["state"] == "Booted"]
                    ready = ready and bool(available)
                    if arguments.simulator_id:
                        selected = find_simulator(devices, arguments.simulator_id)
                        simulator_report["selected"] = selected
                        ready = ready and selected is not None
                        if selected and arguments.bundle_id:
                            app_container = run(
                                [
                                    tools["xcrun"],
                                    "simctl",
                                    "get_app_container",
                                    arguments.simulator_id,
                                    arguments.bundle_id,
                                ]
                            )
                            simulator_report["app_container"] = app_container
                            ready = ready and app_container.get("exit_code") == 0
        report["simulator"] = simulator_report

    if arguments.platform == "macos" and arguments.process_name:
        process = run(["pgrep", "-x", arguments.process_name])
        report["process"] = process
        ready = ready and process.get("exit_code") == 0

    report["ready"] = ready
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
