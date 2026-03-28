import serial.tools.list_ports

def find_flippers():
    return [p.device for p in serial.tools.list_ports.comports() if 'Flipper' in p.description]