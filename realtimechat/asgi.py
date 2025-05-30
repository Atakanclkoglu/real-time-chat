"""
ASGI config for realtimechat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import  AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtimechat.settings')

django.setup() # Bu satır önemli

import chatapp.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chatapp.routing.websocket_urlpatterns
        )
    )
})
