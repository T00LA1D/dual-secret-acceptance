"""Remote logger adapter."""

from datetime import datetime, timezone


def format_remote_log(message: str, level: str = "INFO") -> str:
    now = datetime.now(timezone.utc).isoformat()
    return f"[{now}] {level}: {message}"
