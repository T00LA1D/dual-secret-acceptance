"""Signal capture helpers."""

import time

from .device_interface import send_command


def capture_signal(device, duration=5, poll_interval=0.05):
    """Capture device output for the provided number of seconds."""
    logs = []
    start = time.time()
    while time.time() - start < duration:
        output = send_command(device, "capture")
        if output:
            logs.append(output)
        time.sleep(poll_interval)
    return logs
