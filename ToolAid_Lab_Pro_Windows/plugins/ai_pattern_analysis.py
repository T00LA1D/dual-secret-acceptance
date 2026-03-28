"""Pattern scoring plugin for captured signals."""


def score_signal_patterns(signals: list[str]) -> dict:
    if not signals:
        return {"score": 0.0, "reason": "empty"}
    repetitive = len(signals) - len(set(signals))
    score = max(0.0, 1.0 - repetitive / len(signals))
    return {"score": round(score, 3), "reason": "diversity"}
