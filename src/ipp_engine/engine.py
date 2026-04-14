from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass, field

from .models import AcceptanceRequest, AcceptanceResult
from .policies import AllowAllPolicy, Policy


@dataclass(slots=True)
class IPPEngine:
    """In-memory IPP engine with dual-secret acceptance semantics."""

    policy: Policy = field(default_factory=AllowAllPolicy)
    required_secret_names: tuple[str, str] = ("secret-a", "secret-b")
    _secret_digests: dict[str, str] = field(default_factory=dict, init=False, repr=False)
    _requests: dict[str, AcceptanceRequest] = field(default_factory=dict, init=False, repr=False)

    def register_secret(self, name: str, value: str) -> None:
        if not name:
            raise ValueError("secret name cannot be empty")
        if not value:
            raise ValueError("secret value cannot be empty")
        self._secret_digests[name] = self._digest(value)

    def create_request(self, request_id: str, actor: str, resource: str) -> AcceptanceRequest:
        if request_id in self._requests:
            raise ValueError(f"request already exists: {request_id}")

        request = AcceptanceRequest(request_id=request_id, actor=actor, resource=resource)
        self._requests[request_id] = request
        return request

    def evaluate(self, request_id: str, provided: dict[str, str]) -> AcceptanceResult:
        request = self._requests.get(request_id)
        if request is None:
            return AcceptanceResult(request_id=request_id, accepted=False, reason="request_not_found")

        policy_ok, policy_reason = self.policy.validate(request)
        if not policy_ok:
            return AcceptanceResult(request_id=request_id, accepted=False, reason=policy_reason)

        for required_name in self.required_secret_names:
            stored_digest = self._secret_digests.get(required_name)
            candidate = provided.get(required_name)

            if stored_digest is None:
                return AcceptanceResult(request_id=request_id, accepted=False, reason=f"missing_registered_{required_name}")
            if candidate is None:
                return AcceptanceResult(request_id=request_id, accepted=False, reason=f"missing_provided_{required_name}")
            if not hmac.compare_digest(stored_digest, self._digest(candidate)):
                return AcceptanceResult(request_id=request_id, accepted=False, reason=f"invalid_{required_name}")

        return AcceptanceResult(request_id=request_id, accepted=True, reason="accepted")

    @staticmethod
    def _digest(raw_secret: str) -> str:
        return hashlib.sha256(raw_secret.encode("utf-8")).hexdigest()
