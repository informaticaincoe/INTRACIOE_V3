from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class IsAdminOrSupervisor(BasePermission):
    """Permite acceso solo a usuarios con rol admin o supervisor (o superusuarios)."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return getattr(request.user, 'role', None) in ('admin', 'supervisor')


class IsAuthenticatedReadOrAdminWrite(BasePermission):
    """
    Lectura: cualquier usuario autenticado.
    Escritura (POST/PUT/PATCH/DELETE): solo admin o supervisor.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        return getattr(request.user, 'role', None) in ('admin', 'supervisor')
