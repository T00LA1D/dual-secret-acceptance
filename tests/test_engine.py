from ipp_engine.engine import IPPEngine


def _ready_engine() -> IPPEngine:
    engine = IPPEngine()
    engine.register_secret("secret-a", "alpha")
    engine.register_secret("secret-b", "beta")
    engine.create_request("req-1", actor="integration-test", resource="resource/x")
    return engine


def test_accepts_when_both_secrets_match() -> None:
    engine = _ready_engine()
    result = engine.evaluate("req-1", {"secret-a": "alpha", "secret-b": "beta"})
    assert result.accepted is True
    assert result.reason == "accepted"


def test_rejects_when_one_secret_is_wrong() -> None:
    engine = _ready_engine()
    result = engine.evaluate("req-1", {"secret-a": "alpha", "secret-b": "wrong"})
    assert result.accepted is False
    assert result.reason == "invalid_secret-b"


def test_rejects_when_request_missing() -> None:
    engine = _ready_engine()
    result = engine.evaluate("req-missing", {"secret-a": "alpha", "secret-b": "beta"})
    assert result.accepted is False
    assert result.reason == "request_not_found"
