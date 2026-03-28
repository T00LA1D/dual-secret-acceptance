"""Theme loading and application helper."""

import json
from pathlib import Path


def load_theme(theme_file: str) -> dict:
    path = Path(theme_file)
    if not path.exists():
        return {"theme": "default"}
    return json.loads(path.read_text(encoding="utf-8"))
