import json
from pathlib import Path
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model


class SetupRedirectMiddleware:
    """
    Middleware que revisa el estado de configuración del sistema:
    1. Si no existe db_config.json válido → redirige al paso de base de datos
    2. Si no existe superusuario → redirige al wizard de setup (paso usuario)
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def _db_config_valid(self):
        """Verifica que exista db_config.json con contenido JSON válido."""
        for path in [Path('/app/config/db_config.json'), Path(settings.BASE_DIR) / 'db_config.json']:
            if path.exists():
                try:
                    data = json.loads(path.read_text())
                    if isinstance(data, dict) and data.get('host'):
                        return True
                except (ValueError, json.JSONDecodeError):
                    continue
        return False

    def __call__(self, request):
        # Siempre permitir acceso a /setup/ y archivos estáticos
        if request.path.startswith("/setup/") or request.path.startswith("/static/"):
            return self.get_response(request)

        # Paso 0: verificar config de BD válida
        if not self._db_config_valid():
            return redirect("/setup/?step=database")

        # Paso 1+: verificar que exista al menos un superusuario
        User = get_user_model()
        try:
            if not User.objects.filter(is_superuser=True).exists():
                return redirect("/setup/?step=usuario")
        except Exception:
            return redirect("/setup/?step=usuario")

        return self.get_response(request)
