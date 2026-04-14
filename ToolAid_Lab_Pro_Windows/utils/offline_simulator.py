"""Offline signal simulation helpers."""

from __future__ import annotations

import random


def generate_signals(count: int = 10, seed: int | None = 42):
    rng = random.Random(seed)
    return [f"sig_{idx}_{rng.randint(100, 999)}" for idx in range(count)]


def replay_delay_profile(count: int = 10, base_ms: int = 50):
    return [base_ms + (i % 3) * 10 for i in range(count)]
