def run_experiment(device, signals, loops=3):
    for i in range(loops):
        transmit_signal(device, signals)
        send_command(device, 'verify')