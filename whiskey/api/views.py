import json

from serial import Serial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.renderers import JSONRenderer

import redis

from ..settings import REDIS_URL


def send_command(cmd):
    data = json.dumps(cmd).encode('ascii')
    redis_client.lpush("commands", data)
    _, answer = redis_client.blpop("response")
    answer = json.loads(answer.decode("ascii"))
    return answer


redis_client = redis.StrictRedis.from_url(
    REDIS_URL,
    socket_timeout=1,
    socket_connect_timeout=1,
)
redis_client.delete("commands")
redis_client.delete("response")


class PixelsAPI(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, format=None):
        answer = send_command(request.data)
        return Response(answer, status=200 if answer.get("status") == "ok" else 422)

    def get(self, request, format=None):
        return Response(send_command({"cmd": "get"}))
