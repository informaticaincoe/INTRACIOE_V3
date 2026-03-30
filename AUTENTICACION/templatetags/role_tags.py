from django import template

register = template.Library()


@register.filter
def has_role(user, roles_str):
    """
    Verifica si el usuario tiene uno de los roles indicados.
    Uso: {% if user|has_role:'admin,supervisor' %}
    """
    if not user.is_authenticated:
        return False
    allowed = [r.strip() for r in roles_str.split(',')]
    return getattr(user, 'role', None) in allowed


@register.filter
def has_func(plan_funcs, clave):
    """
    Verifica si el plan incluye una funcionalidad específica.
    Uso: {% if plan_funcs|has_func:'ventas.clientes' %}
    plan_funcs es un set de claves pasado desde el context processor.
    """
    if not plan_funcs:
        return False
    return clave in plan_funcs
