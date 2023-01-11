"""
ASGI config for whiskey project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from .api.consumers import WhiskeyConsumer


os.environ.setdefault("WHISKEY_SETTINGS_MODULE", "whiskey.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws",WhiskeyConsumer.as_asgi()),
    ]),
})
