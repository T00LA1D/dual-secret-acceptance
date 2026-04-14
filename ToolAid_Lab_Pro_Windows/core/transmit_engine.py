"""Signal transmit helpers."""

import time

from .device_interface import send_command


def transmit_signal(device, signals, delay=0.05):
    """Transmit a sequence of signals to a device with a short delay between each."""
    for line in signals:
        send_command(device, f"transmit {line}")
        time.sleep(delay)
