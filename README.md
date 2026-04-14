# ipp-engine

`ipp-engine` is a minimal, production-oriented starter repository for an **IPP (Intent/Policy Processing) engine** with a concrete implementation of **dual-secret acceptance**.

The engine provides:

- A typed domain model for acceptance requests and results.
- A pluggable policy interface for custom validation logic.
- Constant-time secret verification using hashed values.
- A small CLI for local execution and smoke testing.
- Unit tests that capture the core dual-secret behavior.

## Why this exists

This repository was generated from the available context (`dual-secret-acceptance`) and turns that intent into a working, extensible codebase rather than a placeholder.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
python -m ipp_engine --help
```

## Example

```bash
python -m ipp_engine create \
  --request-id req-001 \
  --actor system-a \
  --resource deployment/prod

python -m ipp_engine register --name secret-a --value alpha
python -m ipp_engine register --name secret-b --value beta

python -m ipp_engine evaluate \
  --request-id req-001 \
  --provided secret-a=alpha \
  --provided secret-b=beta
```

## Project structure

```text
src/ipp_engine/
  engine.py      # IPP core orchestration
  models.py      # Domain models and typed outcomes
  policies.py    # Policy abstraction + default policy
  __main__.py    # CLI entrypoint

tests/
  test_engine.py # Dual-secret acceptance tests
```

## Design notes

- **Secret handling:** secrets are stored as SHA-256 digests and compared via `hmac.compare_digest`.
- **Extensibility:** you can inject a custom policy to enforce time windows, actor scopes, quotas, approvals, etc.
- **Determinism:** evaluation returns a structured result with `accepted` plus explicit reason codes.

## Next recommended enhancements

1. Replace in-memory state with a persistence layer (PostgreSQL or Redis).
2. Add request lifecycle APIs (created, pending, consumed, expired).
3. Support KMS-backed key wrapping for at-rest secret protection.
4. Add structured logging, metrics, and tracing hooks.
5. Add HTTP API (FastAPI) for networked usage.
