"""Telemetry app for signal stream stats."""

from core.serial_manager import MockFlipperDevice
from core.signal_processor import capture_signal
from utils.session_analyzer import summarize_logs


def run_telemetry(duration: int = 1):
    device = MockFlipperDevice()
    logs = capture_signal(device, duration=duration)
    return summarize_logs(logs)
