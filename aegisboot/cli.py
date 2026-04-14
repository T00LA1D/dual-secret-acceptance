"""Command-line interface for AegisBoot."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .catalog import BootCatalog


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aegisboot")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Initialize catalog state directory")
    init_cmd.add_argument("--state", required=True, type=Path)

    add_cmd = sub.add_parser("add", help="Add a boot image")
    add_cmd.add_argument("state", type=Path)
    add_cmd.add_argument("image", type=Path)
    add_cmd.add_argument("--label", default=None)

    list_cmd = sub.add_parser("list", help="List registered images")
    list_cmd.add_argument("state", type=Path)

    verify_cmd = sub.add_parser("verify", help="Verify catalog signature")
    verify_cmd.add_argument("state", type=Path)

    menu_cmd = sub.add_parser("build-menu", help="Build deterministic boot menu JSON")
    menu_cmd.add_argument("state", type=Path)
    menu_cmd.add_argument("--output", required=True, type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "init":
        BootCatalog(args.state).init_state()
        print(f"Initialized state: {args.state}")
        return 0

    if args.command == "add":
        catalog = BootCatalog(args.state)
        image = catalog.add_image(args.image, label=args.label)
        print(f"Added: {image.label} ({image.sha256[:12]}…)")
        return 0

    if args.command == "list":
        catalog = BootCatalog(args.state)
        for img in catalog.list_images():
            print(f"- {img['label']} :: {img['file_name']} :: {img['sha256'][:16]}…")
        return 0

    if args.command == "verify":
        catalog = BootCatalog(args.state)
        ok = catalog.verify_catalog()
        print("OK" if ok else "FAIL")
        return 0 if ok else 2

    if args.command == "build-menu":
        catalog = BootCatalog(args.state)
        path = catalog.build_menu(args.output)
        print(f"Wrote menu: {path}")
        return 0

    print("Unsupported command", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
