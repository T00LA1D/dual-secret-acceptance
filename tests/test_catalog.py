from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from aegisboot.catalog import BootCatalog


class CatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = self.root / "state"
        self.image = self.root / "linux.iso"
        self.image.write_bytes(b"sample-iso-content")

    def test_init_add_list_verify_and_build(self) -> None:
        os.environ["AEGISBOOT_MANIFEST_SECRET"] = "test-secret"
        self.addCleanup(lambda: os.environ.pop("AEGISBOOT_MANIFEST_SECRET", None))

        catalog = BootCatalog(self.state)
        catalog.init_state()

        added = catalog.add_image(self.image, label="Ubuntu")
        self.assertEqual(added.label, "Ubuntu")

        images = catalog.list_images()
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]["label"], "Ubuntu")
        self.assertTrue(catalog.verify_catalog())

        menu_path = self.root / "menu.json"
        catalog.build_menu(menu_path)
        menu = json.loads(menu_path.read_text(encoding="utf-8"))
        self.assertEqual(menu["images"][0]["title"], "Ubuntu")

    def test_duplicate_label_rejected(self) -> None:
        os.environ["AEGISBOOT_MANIFEST_SECRET"] = "test-secret"
        self.addCleanup(lambda: os.environ.pop("AEGISBOOT_MANIFEST_SECRET", None))

        catalog = BootCatalog(self.state)
        catalog.init_state()
        catalog.add_image(self.image, label="X")

        another = self.root / "rescue.img"
        another.write_bytes(b"different")

        with self.assertRaises(ValueError):
            catalog.add_image(another, label="X")

    def test_bad_extension_rejected(self) -> None:
        os.environ["AEGISBOOT_MANIFEST_SECRET"] = "test-secret"
        self.addCleanup(lambda: os.environ.pop("AEGISBOOT_MANIFEST_SECRET", None))

        catalog = BootCatalog(self.state)
        catalog.init_state()

        bad = self.root / "note.txt"
        bad.write_text("not bootable", encoding="utf-8")

        with self.assertRaises(ValueError):
            catalog.add_image(bad)

    def test_verify_fails_without_signing_secret(self) -> None:
        catalog = BootCatalog(self.state)
        catalog.init_state()
        self.assertFalse(catalog.verify_catalog())

    def test_add_rejects_tampered_catalog_before_resigning(self) -> None:
        os.environ["AEGISBOOT_MANIFEST_SECRET"] = "test-secret"
        self.addCleanup(lambda: os.environ.pop("AEGISBOOT_MANIFEST_SECRET", None))

        catalog = BootCatalog(self.state)
        catalog.init_state()
        catalog.add_image(self.image, label="Ubuntu")

        catalog_data = json.loads(catalog.state_file.read_text(encoding="utf-8"))
        catalog_data["images"][0]["label"] = "Backdoored"
        catalog.state_file.write_text(
            json.dumps(catalog_data, indent=2), encoding="utf-8"
        )

        another = self.root / "rescue.img"
        another.write_bytes(b"different")

        with self.assertRaises(RuntimeError):
            catalog.add_image(another, label="Rescue")


if __name__ == "__main__":
    unittest.main()
