from serial import Serial
import time
import struct

dev = Serial('/dev/ttyACM1', 115200, timeout=0.25)


def print_messages():
    msg = dev.readline()
    print(msg.decode('ascii'), end='')


def off():
    dev.write(b'\x00')
    print_messages()

def on():
    dev.write(b'\x01')
    print_messages()

def get():
    dev.write(b'\x02')
    print_messages()

def set_pix(pix, r, g, b):
    dev.write(b'\x03' + struct.pack('<BBBB', pix, r, g, b))
    print_messages()


def set_all(colors):
    msg = bytearray(b'\x03')
    for color in colors:
        msg += struct.pack('<BBB', color)
    dev.write(msg)
    print_messages()
