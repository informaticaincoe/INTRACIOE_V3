# AUTENTICACION/urls.py
from django.urls import path
from .views import perfil_usuario_view

urlpatterns = [
    path("cuenta/perfil/", perfil_usuario_view, name="perfil_usuario"),
]
