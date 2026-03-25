import os
import json
from pathlib import Path
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import get_user_model


class SetupRedirectMiddleware:
    """
    Middleware que revisa el estado de configuración del sistema:
    1. Si no hay config de BD (ni env, ni json) → wizard paso database
    2. Si no existe superusuario → wizard paso usuario
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def _db_configured(self):
        """Verifica si la BD está configurada via env o db_config.json."""
        # 1) Variables de entorno (Docker)
        if os.environ.get('DB_HOST') and os.environ.get('DB_NAME'):
            return True

        # 2) db_config.json válido
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
        if request.path.startswith("/setup/") or request.path.startswith("/static/"):
            return self.get_response(request)

        if not self._db_configured():
            return redirect("/setup/?step=database")

        User = get_user_model()
        try:
            if not User.objects.filter(is_superuser=True).exists():
                return redirect("/setup/?step=usuario")
        except Exception:
            return redirect("/setup/?step=usuario")

        return self.get_response(request)
