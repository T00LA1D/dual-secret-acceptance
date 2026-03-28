def capture_signal(device, duration=5):
    import time
    logs = []
    start = time.time()
    while time.time() - start < duration:
        output = send_command(device, 'capture')
        logs.append(output)
    return logs