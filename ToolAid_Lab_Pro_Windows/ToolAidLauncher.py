"""CLI launcher for ToolAid Lab Pro (Linux-friendly)."""

import argparse

from core.experiment_runner import run_experiment
from core.serial_manager import MockFlipperDevice
from core.signal_processor import capture_signal


def build_parser():
    parser = argparse.ArgumentParser(description="ToolAid Lab Pro launcher")
    parser.add_argument("--mode", choices=["capture", "experiment"], default="capture")
    parser.add_argument("--duration", type=int, default=1, help="Capture duration in seconds")
    parser.add_argument("--loops", type=int, default=2, help="Experiment loop count")
    return parser


def main():
    args = build_parser().parse_args()
    device = MockFlipperDevice()

    if args.mode == "capture":
        logs = capture_signal(device, duration=args.duration)
        print("Captured:", logs)
        return 0

    results = run_experiment(device, ["sigA", "sigB"], loops=args.loops)
    print("Experiment results:", results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
