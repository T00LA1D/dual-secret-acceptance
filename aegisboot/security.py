"""Security primitives for catalog integrity."""

from __future__ import annotations

import hashlib
import hmac
import os
from pathlib import Path


DEFAULT_ENV_SECRET = "AEGISBOOT_MANIFEST_SECRET"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _secret_bytes(explicit_secret: str | None = None) -> bytes:
    secret = explicit_secret or os.environ.get(DEFAULT_ENV_SECRET, "")
    if not secret:
        return b""
    return secret.encode("utf-8")


def sign_payload(payload: bytes, explicit_secret: str | None = None) -> str:
    secret = _secret_bytes(explicit_secret)
    if not secret:
        return ""
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()


def verify_payload_signature(
    payload: bytes,
    signature: str,
    explicit_secret: str | None = None,
) -> bool:
    expected = sign_payload(payload, explicit_secret=explicit_secret)
    if not expected:
        return False
    return hmac.compare_digest(expected, signature)
