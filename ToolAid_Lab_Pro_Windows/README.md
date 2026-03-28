# ToolAid Lab Pro Windows

ToolAid Lab Pro is now a functional local tool lab with a runnable CLI, optional GUI, core signal workflows, plugins, and utility modules.

## Features
- Device command bridge with mockable device abstraction.
- Capture + transmit + experiment loops.
- Telemetry summaries and pattern scoring plugins.
- Session logging utilities and JSON/file persistence helpers.
- GUI tabs for dashboard, capture, transmit, automation, response checks, and log viewing.

## Quick start (Linux/macOS)

```bash
cd ToolAid_Lab_Pro_Windows
python ToolAidLauncher.py --mode capture --duration 1
python ToolAidLauncher.py --mode experiment --loops 2
python ToolAidLauncher.py --mode telemetry --duration 1
python ToolAidLauncher.py --mode console
```

## Run desktop GUI

```bash
cd ToolAid_Lab_Pro_Windows
python ToolAidLauncher.py --mode gui
```

## Tests

```bash
cd ToolAid_Lab_Pro_Windows
python -m pytest -q
```
