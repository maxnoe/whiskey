import json

from serial import Serial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.renderers import JSONRenderer

from ..settings import DEVICE


PIXELS = Serial(DEVICE, 115200)


def send_command(cmd):
    data = json.dumps(cmd, separators=(',', ':')).encode("ascii")
    PIXELS.write(data)
    response = PIXELS.readline().decode('ascii')
    if not response.startswith("ok"):
        return {"status": "error", "msg": response}
    return {"status": "ok"}


class PixelsAPI(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, format=None):
        return Response(send_command(request.data))
