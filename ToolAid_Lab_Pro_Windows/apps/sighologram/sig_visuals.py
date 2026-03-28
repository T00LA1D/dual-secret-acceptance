"""Text waveform generation for terminal previews."""


def ascii_wave(samples: list[int], width: int = 40) -> str:
    if not samples:
        return ""
    peak = max(samples) or 1
    rows = []
    for value in samples:
        bars = int((value / peak) * width)
        rows.append("█" * bars)
    return "\n".join(rows)
