#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ipaddress
import json
import urllib.error
import urllib.request
from typing import Any


def inspect_endpoint(host: str, port: int) -> dict[str, Any]:
    host_literal = f"[{host}]" if ":" in host else host
    base = f"http://{host_literal}:{port}"
    result: dict[str, Any] = {"base": base, "reachable": False, "targets": []}
    try:
        with urllib.request.urlopen(f"{base}/json/version", timeout=3) as response:
            result["version"] = json.load(response)
        with urllib.request.urlopen(f"{base}/json/list", timeout=3) as response:
            targets = json.load(response)
        result["targets"] = targets if isinstance(targets, list) else []
        result["reachable"] = True
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
        result["error"] = str(error)
    return result


def match_targets(targets: list[dict[str, Any]], expected_title: str | None, expected_url: str | None) -> list[dict[str, Any]]:
    return [
        target
        for target in targets
        if (not expected_title or expected_title in target.get("title", ""))
        and (not expected_url or expected_url in target.get("url", ""))
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--renderer-port", type=int, required=True)
    parser.add_argument("--main-port", type=int)
    parser.add_argument("--require-main", action="store_true")
    parser.add_argument("--expected-title")
    parser.add_argument("--expected-url")
    arguments = parser.parse_args()

    try:
        loopback = arguments.host.lower() == "localhost" or ipaddress.ip_address(arguments.host).is_loopback
    except ValueError:
        loopback = False
    if not loopback:
        print(json.dumps({"ready": False, "error": "debug endpoint must be loopback-only"}, indent=2))
        return 2

    renderer = inspect_endpoint(arguments.host, arguments.renderer_port)
    main_process = inspect_endpoint(arguments.host, arguments.main_port) if arguments.main_port else None
    matching_targets = match_targets(renderer["targets"], arguments.expected_title, arguments.expected_url)
    renderer["matching_targets"] = matching_targets
    renderer_ready = renderer["reachable"] and bool(matching_targets)
    main_ready = bool(main_process and main_process["reachable"] and main_process["targets"])
    ready = renderer_ready and (main_ready if arguments.require_main else True)
    print(
        json.dumps(
            {"ready": ready, "renderer": renderer, "main": main_process},
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
