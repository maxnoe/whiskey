import json
import struct

from serial import Serial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.renderers import JSONRenderer

from ..settings import DEVICE


PIXELS = Serial(DEVICE, 115200)


def get_response():
    msg = PIXELS.readline().decode('ascii')
    status, _, msg = msg.partition(': ')
    return status, msg


def off():
    PIXELS.write(b'\x00')
    return get_response()

def on():
    PIXELS.write(b'\x01')
    return get_response()

def get():
    PIXELS.write(b'\x02')
    status, msg = get_response()
    print(status, msg)
    return status, json.loads(msg)

def set_pix(pix, r, g, b):
    PIXELS.write(b'\x03' + struct.pack('<BBBB', pix, r, g, b))
    return get_response()


def set_all(colors):
    msg = bytearray(b'\x04')
    for color in colors:
        msg += struct.pack('<BBB', *color)
    PIXELS.write(msg)
    return get_response()


def parse_color(color):
    if color is None:
        raise ValueError('missing color')

    if not isinstance(color, (tuple, list)):
        raise ValueError('invalid color')

    if len(color) != 3:
        raise ValueError('color data has wrong length')

    return color


class PixelsAPI(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, format=None):
        cmd = request.data.get("cmd")
        if cmd is None:
            return Response({'status': 'error', 'msg': 'required arg cmd missing'})
        msg = ''
        status = 'error'
        match cmd:
            case 'on':
                status, msg = on()
            case 'off':
                status, msg = off()
            case 'get':
                status, data = get()
                return Response({'status': status, **data})
            case 'set_pix':
                pix = request.data.get('pix')
                if pix is None:
                    return Response({'status': 'error', 'msg': 'pix missing'})

                try:
                    r, g, b = parse_color(request.data.get('color'))
                except ValueError as e:
                    return Response({'status': 'error', 'msg': str(e)})

                status, msg = set_pix(pix, r, g, b)
            case _:
                status, msg = 'error', 'invalid command'                

        return Response({'status': status, 'msg': msg})

    def get(self, request, format=None):
        status, msg = get()
        return Response({'status': status, 'msg': msg})
