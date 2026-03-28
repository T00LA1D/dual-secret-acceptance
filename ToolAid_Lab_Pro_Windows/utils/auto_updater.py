"""Simple semantic version check utility."""

from __future__ import annotations


def check_update(current_version: str, latest_version: str) -> bool:
    return tuple(map(int, current_version.split("."))) < tuple(
        map(int, latest_version.split("."))
    )
