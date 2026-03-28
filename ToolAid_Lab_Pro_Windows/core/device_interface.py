def send_command(device, cmd):
    device.write((cmd + '\n').encode())
    return device.read_all().decode()