def transmit_signal(device, signals):
    import time
    for line in signals:
        send_command(device, f'transmit {line}')
        time.sleep(0.05)