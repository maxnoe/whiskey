from serial import Serial
import json
import msgpack
import time

dev = Serial('/dev/ttyACM0', 115200)

def send_command(cmd):
    data = json.dumps(cmd, separators=(",", ":")).encode('ascii')

    print("Send  data:", data)
    n = dev.write(data)
    print("bytes written:", n)
    print(dev.readline().decode('ascii') + dev.read_all().decode('ascii'))


colors = [(0, 0, 40)] * 7 + [(40, 0, 0)] * 7
