from django.urls import re_path

from .consumers import WhiskeyConsumer


websocket_urlpatterns = [
    re_path(r"socket", WhiskeyConsumer.as_asgi()),
]
