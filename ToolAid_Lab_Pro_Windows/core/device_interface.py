"""Device communication primitives."""


def send_command(device, cmd):
    """Send a command to a connected device and return decoded output."""
    device.write((cmd + "\n").encode())
    return device.read_all().decode(errors="replace").strip()
