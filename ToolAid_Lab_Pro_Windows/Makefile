.PHONY: install test run-capture run-console run-telemetry

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	python -m pytest -q

run-capture:
	python ToolAidLauncher.py --mode capture --duration 1

run-console:
	python ToolAidLauncher.py --mode console

run-telemetry:
	python ToolAidLauncher.py --mode telemetry --duration 1
