from django.urls import re_path
from .consumers import CocinaComandasConsumer, MeseroNotifsConsumer

websocket_urlpatterns = [
    re_path(r"ws/cocina/comandas/$", CocinaComandasConsumer.as_asgi()),
    re_path(r"ws/mesero/notifs/$", MeseroNotifsConsumer.as_asgi()),
]
