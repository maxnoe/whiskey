import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import redis

from ..settings import REDIS_URL


def send_command(cmd):
    data = json.dumps(cmd).encode('ascii')

    try:
        redis_client.lpush("commands", data)
        _, answer = redis_client.blpop("response")
    except redis.TimeoutError:
        return {
            "status": "error",
            "status_code": 503,
            "msg": "Error connecting to redis"
        }

    answer = json.loads(answer.decode("ascii"))
    answer["status_code"] = 200 if answer["status"] == "ok" else 422
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
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request, format=None):
        cmd = request.data
        answer = send_command(request.data)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("whiskey", {"type": "update"})
        return Response(answer, status=answer["status_code"])

    def get(self, request, format=None):
        answer = send_command({"cmd": "get"})
        return Response(answer)
