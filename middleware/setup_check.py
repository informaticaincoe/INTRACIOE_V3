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

    def _db_config_exists(self):
        """Busca db_config.json en el volumen Docker o en la raíz del proyecto."""
        return (
            Path('/app/config/db_config.json').exists()
            or (Path(settings.BASE_DIR) / 'db_config.json').exists()
        )

    def __call__(self, request):
        # Siempre permitir acceso a /setup/ y archivos estáticos
        if request.path.startswith("/setup/") or request.path.startswith("/static/"):
            return self.get_response(request)

        # Paso 0: verificar que exista la configuración de BD
        if not self._db_config_exists():
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
