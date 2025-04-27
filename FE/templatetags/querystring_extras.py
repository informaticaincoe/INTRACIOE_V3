from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def remove_query_param(context, param):
    """
    Devuelve la cadena de consulta (querystring) actual sin el parámetro dado.
    """
    request = context['request']
    query_params = request.GET.copy()
    if param in query_params:
        query_params.pop(param)
    return query_params.urlencode()
