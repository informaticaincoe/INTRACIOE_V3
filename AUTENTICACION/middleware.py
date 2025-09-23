from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from FE.models import Emisor_fe
from AUTENTICACION.models import ConfiguracionServidor, UsuarioEmisor

User = get_user_model()

class InitialSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Evitar bucle infinito con la vista de setup
        if request.path.startswith(reverse("setup_wizard")):
            return self.get_response(request)

        # Validar si ya existe configuración mínima
        if not User.objects.filter(role="admin").exists() \
           or not Emisor_fe.objects.exists() \
           or not UsuarioEmisor.objects.exists() \
           or not ConfiguracionServidor.objects.exists():
            return redirect("setup_wizard")

        return self.get_response(request)
