"""Experiment loop orchestration."""

from .device_interface import send_command
from .transmit_engine import transmit_signal


def run_experiment(device, signals, loops=3):
    """Run transmit/verify loops and return verification outputs."""
    results = []
    for _ in range(loops):
        transmit_signal(device, signals)
        results.append(send_command(device, "verify"))
    return results
