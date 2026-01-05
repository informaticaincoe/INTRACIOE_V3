from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def role_required(*roles):
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
