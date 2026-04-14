"""Interactive lab console for quick command execution."""

from core.device_interface import send_command
from core.serial_manager import MockFlipperDevice


def run_console(commands: list[str] | None = None):
    device = MockFlipperDevice()
    commands = commands or ["capture", "verify"]
    return [send_command(device, cmd) for cmd in commands]
