from __future__ import annotations

from dataclasses import dataclass

from .models import AcceptanceRequest


class Policy:
    """Base policy interface for acceptance checks beyond raw secret matching."""

    def validate(self, request: AcceptanceRequest) -> tuple[bool, str]:
        raise NotImplementedError


@dataclass(slots=True)
class AllowAllPolicy(Policy):
    """Default policy that allows every structurally valid request."""

    def validate(self, request: AcceptanceRequest) -> tuple[bool, str]:
        if not request.request_id or not request.actor or not request.resource:
            return False, "invalid_request"
        return True, "ok"
