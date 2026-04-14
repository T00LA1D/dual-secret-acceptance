"""Catalog management for bootable images."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from .security import sha256_file, sign_payload, verify_payload_signature


ALLOWED_EXTENSIONS = {".iso", ".img", ".vhd", ".vhdx", ".wim", ".efi"}
STATE_FILE_NAME = "catalog.json"


@dataclass
class BootImage:
    label: str
    source_path: str
    file_name: str
    size_bytes: int
    sha256: str
    extension: str


@dataclass
class BootCatalog:
    state_dir: Path
    policy: dict[str, Any] = field(
        default_factory=lambda: {
            "require_signature": True,
            "allow_legacy_images": False,
        }
    )

    def __post_init__(self) -> None:
        self.state_dir = Path(self.state_dir)
        self.state_file = self.state_dir / STATE_FILE_NAME

    @staticmethod
    def _safe_file_name(path: Path) -> str:
        name = path.name
        if not name or name in {".", ".."}:
            raise ValueError("Unsafe image name")
        if "/" in name or "\\" in name:
            raise ValueError("Unsafe separator in image name")
        return name

    @staticmethod
    def _normalize_label(path: Path, custom_label: str | None) -> str:
        if custom_label:
            label = custom_label.strip()
            if not label:
                raise ValueError("Label cannot be empty")
            return label
        return path.stem

    def init_state(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        if self.state_file.exists():
            return
        catalog = {
            "version": 1,
            "policy": self.policy,
            "images": [],
            "signature": "",
        }
        self._write_catalog(catalog)

    def _read_catalog(self) -> dict[str, Any]:
        if not self.state_file.exists():
            raise FileNotFoundError(
                f"State not initialized at {self.state_file}. Run init first."
            )
        return json.loads(self.state_file.read_text(encoding="utf-8"))

    def _signed_payload(self, catalog: dict[str, Any]) -> bytes:
        signing_view = dict(catalog)
        signing_view.pop("signature", None)
        return json.dumps(signing_view, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )

    def _write_catalog(self, catalog: dict[str, Any]) -> None:
        payload = self._signed_payload(catalog)
        catalog["signature"] = sign_payload(payload)
        self.state_file.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

    def _catalog_signature_valid(self, catalog: dict[str, Any]) -> bool:
        payload = self._signed_payload(catalog)
        signature = catalog.get("signature", "")
        return verify_payload_signature(payload, signature)

    def verify_catalog(self) -> bool:
        catalog = self._read_catalog()
        return self._catalog_signature_valid(catalog)

    def add_image(self, image_path: Path, label: str | None = None) -> BootImage:
        image_path = Path(image_path)
        if not image_path.exists() or not image_path.is_file():
            raise FileNotFoundError(f"Image not found: {image_path}")

        ext = image_path.suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported extension '{ext}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}"
            )

        file_name = self._safe_file_name(image_path)
        image = BootImage(
            label=self._normalize_label(image_path, label),
            source_path=str(image_path.resolve()),
            file_name=file_name,
            size_bytes=image_path.stat().st_size,
            sha256=sha256_file(image_path),
            extension=ext,
        )

        catalog = self._read_catalog()
        if catalog.get("policy", {}).get(
            "require_signature", True
        ) and not self._catalog_signature_valid(catalog):
            raise RuntimeError("Catalog integrity verification failed")

        images = catalog.setdefault("images", [])

        for existing in images:
            if existing["sha256"] == image.sha256:
                raise ValueError(
                    f"Image already present with identical digest: {image.sha256}"
                )
            if existing["label"] == image.label:
                raise ValueError(f"Duplicate label not allowed: {image.label}")

        images.append(image.__dict__)
        self._write_catalog(catalog)
        return image

    def list_images(self) -> list[dict[str, Any]]:
        catalog = self._read_catalog()
        return list(catalog.get("images", []))

    def build_menu(self, output_path: Path) -> Path:
        output_path = Path(output_path)
        catalog = self._read_catalog()

        if self.policy.get("require_signature", True) and not self._catalog_signature_valid(
            catalog
        ):
            raise RuntimeError("Catalog integrity verification failed")

        menu = {
            "menu_version": 1,
            "generated_from": str(self.state_file.resolve()),
            "images": [
                {
                    "title": img["label"],
                    "device_path": img["source_path"],
                    "expected_sha256": img["sha256"],
                    "type": img["extension"],
                }
                for img in catalog.get("images", [])
            ],
        }
        output_path.write_text(json.dumps(menu, indent=2), encoding="utf-8")
        return output_path
