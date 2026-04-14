"""Coordinate multiple devices in lockstep."""

from core.device_interface import send_command


def broadcast(devices, command: str):
    return [send_command(device, command) for device in devices]
