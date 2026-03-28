"""Serial port discovery and lightweight simulation support."""

try:
    import serial.tools.list_ports
except ImportError:  # pyserial may not be installed in all environments
    serial = None


class MockFlipperDevice:
    """Simple in-memory mock for local Linux testing without hardware."""

    def __init__(self):
        self._buffer = b""

    def write(self, payload):
        message = payload.decode(errors="replace").strip()
        if message == "capture":
            self._buffer = b"mock_signal\n"
        elif message.startswith("transmit "):
            self._buffer = b"ok\n"
        elif message == "verify":
            self._buffer = b"verified\n"
        else:
            self._buffer = b"unknown\n"

    def read_all(self):
        out = self._buffer
        self._buffer = b""
        return out


def find_flippers():
    """Return detected Flipper-like serial devices."""
    if serial is None:
        return []

    return [
        p.device
        for p in serial.tools.list_ports.comports()
        if "Flipper" in (p.description or "")
    ]
