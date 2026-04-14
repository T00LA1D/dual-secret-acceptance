from __future__ import annotations

import argparse
import json
from typing import Any

from .engine import IPPEngine


ENGINE = IPPEngine()


def _kv_pairs(values: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"invalid key=value pair: {item}")
        key, val = item.split("=", 1)
        out[key] = val
    return out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="IPP dual-secret acceptance engine")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create a new acceptance request")
    create.add_argument("--request-id", required=True)
    create.add_argument("--actor", required=True)
    create.add_argument("--resource", required=True)

    register = sub.add_parser("register", help="Register a secret for later evaluation")
    register.add_argument("--name", required=True)
    register.add_argument("--value", required=True)

    evaluate = sub.add_parser("evaluate", help="Evaluate request against provided secrets")
    evaluate.add_argument("--request-id", required=True)
    evaluate.add_argument("--provided", action="append", default=[], help="key=value pairs")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "create":
            req = ENGINE.create_request(args.request_id, args.actor, args.resource)
            payload: dict[str, Any] = {
                "request_id": req.request_id,
                "actor": req.actor,
                "resource": req.resource,
                "created_at": req.created_at.isoformat(),
            }
        elif args.command == "register":
            ENGINE.register_secret(args.name, args.value)
            payload = {"status": "ok", "name": args.name}
        elif args.command == "evaluate":
            result = ENGINE.evaluate(args.request_id, _kv_pairs(args.provided))
            payload = {
                "request_id": result.request_id,
                "accepted": result.accepted,
                "reason": result.reason,
                "evaluated_at": result.evaluated_at.isoformat(),
            }
        else:
            parser.error("unsupported command")
            return 2
    except ValueError as exc:
        payload = {"status": "error", "message": str(exc)}
        print(json.dumps(payload))
        return 1

    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
