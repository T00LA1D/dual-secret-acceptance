"""SharkleberryFin controller app."""

from core.serial_manager import MockFlipperDevice
from core.transmit_engine import transmit_signal


def run_shark_mode(signals: list[str]):
    device = MockFlipperDevice()
    transmit_signal(device, signals)
    return {"transmitted": len(signals)}
