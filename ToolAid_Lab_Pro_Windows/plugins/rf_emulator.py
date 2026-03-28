"""RF emulation plugin."""


def emulate_rf_frame(raw_signal: str) -> str:
    return f"rf::{raw_signal}"
