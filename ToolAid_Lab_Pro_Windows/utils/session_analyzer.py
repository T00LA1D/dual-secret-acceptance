"""Session analytics for captured logs."""

from __future__ import annotations

from collections import Counter


def summarize_logs(logs: list[str]) -> dict:
    c = Counter(logs)
    return {
        "entries": len(logs),
        "unique_entries": len(c),
        "top_entries": c.most_common(5),
    }
