import subprocess
import sys
from pathlib import Path

from core.experiment_runner import run_experiment
from core.serial_manager import MockFlipperDevice
from core.signal_processor import capture_signal


ROOT = Path(__file__).resolve().parents[1]


def test_capture_signal_returns_mock_data():
    device = MockFlipperDevice()
    logs = capture_signal(device, duration=0)
    assert logs == []


def test_run_experiment_returns_verified():
    device = MockFlipperDevice()
    out = run_experiment(device, ["a", "b"], loops=2)
    assert out == ["verified", "verified"]


def test_launcher_capture_mode_runs():
    result = subprocess.run(
        [sys.executable, "ToolAidLauncher.py", "--mode", "capture", "--duration", "1"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Captured:" in result.stdout
