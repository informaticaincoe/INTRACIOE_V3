# AUTENTICACION/email_utils.py
from django.conf import settings
from django.core.mail import get_connection

from django.core.cache import cache
from .models import EmailProfile

CACHE_KEY_FMT = "email_profile_active:{scope}"
CACHE_TTL = 60  # seg

def get_active_email_profile(scope: str):
    """Devuelve el EmailProfile activo para el scope dado o None."""
    key = CACHE_KEY_FMT.format(scope=scope)
    prof = cache.get(key)
    if prof is not None:
        return prof

    prof = EmailProfile.objects.filter(scope=scope, is_active=True).order_by('-updated_at').first()
    cache.set(key, prof, CACHE_TTL)
    return prof

def get_smtp_connection_for(scope: str):
    """
    Devuelve (connection, from_email) para el scope ('fe' o 'general'):
    - Usa perfil activo en BD si existe.
    - Fallback a settings si no.
    """
    prof = get_active_email_profile(scope)

    if prof:
        conn = get_connection(
            backend=getattr(settings, "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"),
            host=prof.host,
            port=prof.port,
            username=prof.username,
            password=prof.password,
            use_ssl=prof.use_ssl,
            use_tls=prof.use_tls,
            timeout=getattr(settings, "EMAIL_TIMEOUT", None),
        )
        return conn, (prof.from_email or prof.username)

    # ---- Fallback a settings.py ----
    if scope == 'fe':
        host = getattr(settings, "EMAIL_HOST_FE", None) or getattr(settings, "EMAIL_HOST", "")
        port = getattr(settings, "EMAIL_PORT_FE", None) or getattr(settings, "EMAIL_PORT", 465)
        use_ssl = getattr(settings, "EMAIL_USE_SSL_FE", None)
        if use_ssl is None: use_ssl = getattr(settings, "EMAIL_USE_SSL", True)
        use_tls = getattr(settings, "EMAIL_USE_TLS_FE", None)
        if use_tls is None: use_tls = getattr(settings, "EMAIL_USE_TLS", False)
        username = getattr(settings, "EMAIL_HOST_USER_FE", None) or getattr(settings, "EMAIL_HOST_USER", "")
        password = getattr(settings, "EMAIL_HOST_PASSWORD_FE", None) or getattr(settings, "EMAIL_HOST_PASSWORD", "")
        from_email = username or getattr(settings, "DEFAULT_FROM_EMAIL", "")
    else:
        host = getattr(settings, "EMAIL_HOST", "")
        port = getattr(settings, "EMAIL_PORT", 465)
        use_ssl = getattr(settings, "EMAIL_USE_SSL", True)
        use_tls = getattr(settings, "EMAIL_USE_TLS", False)
        username = getattr(settings, "EMAIL_HOST_USER", "")
        password = getattr(settings, "EMAIL_HOST_PASSWORD", "")
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "") or username

    conn = get_connection(
        backend=getattr(settings, "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"),
        host=host, port=port, username=username, password=password,
        use_ssl=use_ssl, use_tls=use_tls, timeout=getattr(settings, "EMAIL_TIMEOUT", None),
    )
    return conn, from_email
