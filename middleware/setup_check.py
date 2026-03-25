from pathlib import Path
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model


class SetupRedirectMiddleware:
    """
    Middleware que revisa el estado de configuración del sistema:
    1. Si no existe db_config.json → redirige al paso de base de datos
    2. Si no existe superusuario → redirige al wizard de setup (paso usuario)
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Siempre permitir acceso a /setup/ y archivos estáticos
        if request.path.startswith("/setup/") or request.path.startswith("/static/"):
            return self.get_response(request)

        # Paso 0: verificar que exista la configuración de BD
        db_config_path = Path(settings.BASE_DIR) / 'db_config.json'
        if not db_config_path.exists():
            return redirect("/setup/?step=database")

        # Paso 1+: verificar que exista al menos un superusuario
        User = get_user_model()
        try:
            existe_super = User.objects.filter(is_superuser=True).exists()
        except Exception:
            existe_super = False

        if not existe_super:
            return redirect("/setup/?step=usuario")

        return self.get_response(request)
