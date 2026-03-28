import subprocess
import sys
from pathlib import Path

from apps.lab_console.console_main import run_console
from apps.sighologram.sig_main import run_telemetry
from core.experiment_runner import run_experiment
from core.serial_manager import MockFlipperDevice
from core.signal_processor import capture_signal
from plugins.ai_pattern_analysis import score_signal_patterns
from plugins.nfc_handler import decode_nfc_uid
from plugins.rf_emulator import emulate_rf_frame
from utils.offline_simulator import generate_signals
from utils.session_analyzer import summarize_logs

ROOT = Path(__file__).resolve().parents[1]


def test_capture_signal_returns_mock_data():
    device = MockFlipperDevice()
    logs = capture_signal(device, duration=0)
    assert logs == []


def test_run_experiment_returns_verified():
    device = MockFlipperDevice()
    out = run_experiment(device, ["a", "b"], loops=2)
    assert out == ["verified", "verified"]


def test_plugins_and_utils_are_functional():
    assert emulate_rf_frame("abc") == "rf::abc"
    assert decode_nfc_uid("AA BB") == {"uid": "aabb", "length": 2}
    signals = generate_signals(count=3, seed=7)
    assert len(signals) == 3
    summary = summarize_logs(["x", "x", "y"])
    assert summary["entries"] == 3
    assert score_signal_patterns(["x", "y"])["score"] > 0


def test_app_modules_return_data():
    assert run_console(["capture", "verify"]) == ["mock_signal", "verified"]
    telemetry = run_telemetry(duration=0)
    assert telemetry["entries"] == 0


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


def test_launcher_console_and_telemetry_modes_run():
    for mode in ("console", "telemetry"):
        cmd = [sys.executable, "ToolAidLauncher.py", "--mode", mode]
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
        assert result.returncode == 0
