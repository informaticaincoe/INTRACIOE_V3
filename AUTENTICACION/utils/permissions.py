from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """Verifica que el usuario tenga uno de los roles indicados."""
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            if getattr(user, "role", None) not in roles:
                raise PermissionDenied("No tienes permisos para acceder a esta página.")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def plan_module_required(module_field):
    """
    Verifica que el plan del emisor tenga el módulo habilitado.
    module_field: nombre del campo booleano, ej. 'tiene_restaurante'.
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            from FE.models import Emisor_fe
            try:
                emisor = Emisor_fe.objects.first()
                if emisor:
                    suscripcion = getattr(emisor, 'suscripcion', None)
                    if suscripcion and suscripcion.esta_vigente():
                        if getattr(suscripcion.plan, module_field, False):
                            return view_func(request, *args, **kwargs)
            except Exception:
                pass
            raise PermissionDenied("Su plan no incluye acceso a este módulo.")
        return _wrapped
    return decorator


def restaurant_permission(*roles):
    """
    Decorador combinado para vistas de restaurante:
    - Requiere login
    - Requiere rol en la lista (o superuser)
    - Requiere plan.tiene_restaurante = True
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            # Verificar rol
            if getattr(user, "role", None) not in roles:
                raise PermissionDenied("No tienes permisos para acceder a esta página.")
            # Verificar plan
            from FE.models import Emisor_fe
            try:
                emisor = Emisor_fe.objects.first()
                if emisor:
                    suscripcion = getattr(emisor, 'suscripcion', None)
                    if suscripcion and suscripcion.esta_vigente():
                        if getattr(suscripcion.plan, 'tiene_restaurante', False):
                            return view_func(request, *args, **kwargs)
            except Exception:
                pass
            raise PermissionDenied("Su plan no incluye acceso al módulo de restaurante.")
        return _wrapped
    return decorator
