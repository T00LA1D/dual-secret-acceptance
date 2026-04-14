# Contributing

## Setup
1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development checks
```bash
python -m pytest -q
python ToolAidLauncher.py --mode capture --duration 1
```

## Pull requests
- Keep changes focused.
- Include tests for behavior changes.
- Update README when user-facing behavior changes.
