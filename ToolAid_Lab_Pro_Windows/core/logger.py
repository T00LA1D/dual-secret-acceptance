"""Tiny file logger utility."""


def log_message(path, msg):
    with open(path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
