from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from FE.models import Emisor_fe


class DemoProtectionMiddleware:
    """
    En modo demo, bloquea operaciones destructivas (DELETE)
    sobre datos existentes. Permite crear nuevos registros.
    """
    PROTECTED_KEYWORDS = ['eliminar', 'delete', 'anular', 'borrar']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo interceptar en modo demo + métodos destructivos
        if request.method in ('DELETE',) or (
            request.method == 'POST' and
            any(kw in request.path.lower() for kw in self.PROTECTED_KEYWORDS)
        ):
            try:
                emisor = Emisor_fe.objects.first()
                if emisor and emisor.modo_demo:
                    # Permitir al admin de Django gestionar todo
                    if request.path.startswith('/admin/'):
                        return self.get_response(request)

                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'error': 'Operación no permitida en modo demostración.'
                        }, status=403)

                    messages.warning(
                        request,
                        'Esta operación no está permitida en modo demostración.'
                    )
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            except Exception:
                pass

        return self.get_response(request)
