#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class DelegationProfile:
    meaningful_streams: int
    specialist_review: bool
    repositories: int
    independent_units: int
    high_risk: bool


def recommend_children(profile: DelegationProfile) -> tuple[int, str]:
    values = {"meaningful streams": profile.meaningful_streams, "independent units": profile.independent_units}
    for label, value in values.items():
        if value < 0:
            raise ValueError(f"{label} must not be negative")
    if profile.repositories < 1:
        raise ValueError("repositories must be at least one")
    if profile.meaningful_streams == 0:
        return 0, "no meaningful evidence stream"
    if profile.high_risk and profile.independent_units > 0:
        return min(3, profile.meaningful_streams, profile.independent_units), "high-risk independent units"
    if profile.repositories > 1:
        return min(2, profile.meaningful_streams, profile.repositories), "cross-repository investigation"
    if profile.specialist_review:
        return 1, "specialist evidence stream"
    return 0, "direct parent work"


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Recommend the hoyelam-stack default Codex child count",
        epilog=(
            "Examples: no flags routes a simple parent operation to 0; "
            "--meaningful-streams 1 --specialist-review routes 1; "
            "--meaningful-streams 2 --repositories 2 routes 2; "
            "--meaningful-streams 3 --independent-units 3 --high-risk routes 3. "
            "High-risk independent units take precedence over cross-repository and specialist signals."
        ),
    )
    root.add_argument(
        "--meaningful-streams",
        type=int,
        default=0,
        help="bounded evidence streams whose results can change the parent decision",
    )
    root.add_argument(
        "--specialist-review",
        action="store_true",
        help="one stream requires specialist judgment independent from the parent",
    )
    root.add_argument(
        "--repositories",
        type=int,
        default=1,
        help="repositories that require independent investigation; must be at least one",
    )
    root.add_argument(
        "--independent-units",
        type=int,
        default=0,
        help="high-risk units that can run without shared writes or sequential dependencies",
    )
    root.add_argument(
        "--high-risk",
        action="store_true",
        help="the task benefits from independent evidence because impact or uncertainty is high",
    )
    return root


def main() -> int:
    arguments = parser().parse_args()
    try:
        children, reason = recommend_children(
            DelegationProfile(
                meaningful_streams=arguments.meaningful_streams,
                specialist_review=arguments.specialist_review,
                repositories=arguments.repositories,
                independent_units=arguments.independent_units,
                high_risk=arguments.high_risk,
            )
        )
    except ValueError as error:
        parser().error(str(error))
    print(json.dumps({"children": children, "reason": reason}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
