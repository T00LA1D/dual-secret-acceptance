"""CLI/GUI launcher for ToolAid Lab Pro."""

import argparse

from apps.lab_console.console_main import run_console
from apps.sighologram.sig_main import run_telemetry
from core.experiment_runner import run_experiment
from core.serial_manager import MockFlipperDevice
from core.signal_processor import capture_signal
from plugins.ai_pattern_analysis import score_signal_patterns


def build_parser():
    parser = argparse.ArgumentParser(description="ToolAid Lab Pro launcher")
    parser.add_argument(
        "--mode",
        choices=["capture", "experiment", "console", "telemetry", "gui"],
        default="capture",
    )
    parser.add_argument("--duration", type=int, default=1, help="Capture duration in seconds")
    parser.add_argument("--loops", type=int, default=2, help="Experiment loop count")
    return parser


def main():
    args = build_parser().parse_args()
    device = MockFlipperDevice()

    if args.mode == "capture":
        logs = capture_signal(device, duration=args.duration)
        print("Captured:", logs)
        print("Pattern score:", score_signal_patterns(logs))
        return 0

    if args.mode == "experiment":
        results = run_experiment(device, ["sigA", "sigB"], loops=args.loops)
        print("Experiment results:", results)
        return 0

    if args.mode == "console":
        print("Console outputs:", run_console())
        return 0

    if args.mode == "telemetry":
        print("Telemetry:", run_telemetry(duration=args.duration))
        return 0

    try:
        from gui.main_window import run_gui
    except ModuleNotFoundError as exc:
        print("GUI mode requires PySide6:", exc)
        return 1
    return run_gui()


if __name__ == "__main__":
    raise SystemExit(main())
