"""
ASGI config for intracoe project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import sys
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import RESTAURANTE.routing

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../FE')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intracoe.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(RESTAURANTE.routing.websocket_urlpatterns)
    ),
})