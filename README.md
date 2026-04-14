# AegisBoot (prototype)

AegisBoot is a **cross-platform boot image catalog and hardened menu builder** prototype.

It is inspired by Ventoy-style workflows (drop many ISO/IMG files in one place and select at boot), but this repo focuses on the hardening layer:

- Immutable image inventory with SHA-256 measurement
- Signed manifest (`HMAC-SHA256`) to detect tampering
- Strict filename/path validation to block traversal tricks
- Deterministic menu generation from a trusted manifest
- Optional policy flags (`require_signature`, `allow_legacy_images`)

> ⚠️ This is an application-layer prototype and **not yet a full replacement bootloader**.
> It does not overwrite MBR/GPT/UEFI firmware entries directly yet.

## Why this direction

A true replacement for GRUB/Ventoy needs:

1. A pre-OS boot stage (UEFI app / shim / secure boot chain)
2. Verified cryptographic trust roots
3. Platform-specific installers for Linux, Windows, and macOS
4. Recovery and anti-bricking workflows

This repository delivers a secure control-plane first so the boot-stage can later consume trusted metadata.

## Quickstart

```bash
python3 -m aegisboot.cli init --state ./state
python3 -m aegisboot.cli add ./state /path/to/ubuntu.iso --label "Ubuntu 24.04"
python3 -m aegisboot.cli add ./state /path/to/memtest.img
python3 -m aegisboot.cli list ./state
python3 -m aegisboot.cli build-menu ./state --output ./boot-menu.json
```

To enforce manifest integrity, set a secret:

```bash
export AEGISBOOT_MANIFEST_SECRET="replace-with-long-random-secret"
python3 -m aegisboot.cli verify ./state
```

## Security notes

- Never store the signing secret on the target removable media.
- Use per-device secrets for better blast-radius control.
- Store images on a filesystem with integrity features where possible.
- Pair this with Secure Boot in production.

## Development

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```
