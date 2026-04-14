# ToolAid Lab Pro Windows

A functional ToolAid Lab repository with runnable CLI workflows, optional GUI mode, modular core services, plugins, utilities, and test coverage.

## Repository readiness
This project now includes standard GitHub repository files:
- `.github/workflows/ci.yml` (CI test workflow)
- Issue templates + PR template
- `CONTRIBUTING.md`, `SECURITY.md`, `CODEOWNERS`
- `.gitignore`, `.editorconfig`, `.gitattributes`
- `pyproject.toml` and `Makefile`

## Quick start
```bash
cd ToolAid_Lab_Pro_Windows
pip install -r requirements.txt
python ToolAidLauncher.py --mode capture --duration 1
python ToolAidLauncher.py --mode experiment --loops 2
python ToolAidLauncher.py --mode console
python ToolAidLauncher.py --mode telemetry --duration 1
```

## GUI mode
```bash
python ToolAidLauncher.py --mode gui
```
> Requires `PySide6`.

## Tests
```bash
python -m pytest -q
```

## Create and push as a new GitHub repo
```bash
cd ToolAid_Lab_Pro_Windows
git init
git add .
git commit -m "Initial ToolAid Lab Pro repo"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```
