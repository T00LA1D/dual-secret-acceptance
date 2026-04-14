from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class AcceptanceRequest:
    """Represents an acceptance request that must be evaluated by policy."""

    request_id: str
    actor: str
    resource: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class AcceptanceResult:
    """Structured evaluation output for deterministic downstream handling."""

    request_id: str
    accepted: bool
    reason: str
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
