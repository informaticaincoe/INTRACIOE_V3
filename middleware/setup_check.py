from django.shortcuts import redirect
from django.contrib.auth import get_user_model

class SetupRedirectMiddleware:
    """
    Middleware que revisa si hay al menos un superusuario creado.
    Si no existe, redirige siempre al wizard de setup.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        User = get_user_model()

        try:
            existe_super = User.objects.filter(is_superuser=True).exists()
        except Exception:
            # Si la base todavía no está inicializada
            existe_super = False

        # Permitir acceder a /setup/ sin importar nada
        if request.path.startswith("/setup/"):
            return self.get_response(request)

        # Si no hay superusuario, redirigir siempre al setup
        if not existe_super:
            return redirect("/setup/?step=usuario")

        return self.get_response(request)

