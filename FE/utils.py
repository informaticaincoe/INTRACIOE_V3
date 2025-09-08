# views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Si creaste el mapeo UsuarioEmisor(user -> emisor) como sugerimos:
from AUTENTICACION.models import UsuarioEmisor  # ajusta al path real
from FE.models import Emisor_fe  # ajusta al path real

def _get_emisor_for_user(user, estricto=True):
    """
    Devuelve el Emisor_fe asociado al usuario.
    Estrategia:
      1) UsuarioEmisor (si existe el mapeo).
      2) (Opcional) user.perfilusuario.emisor_preferido si lo tienes.
      3) Fallback: None (estricto=True) o el primer emisor (estricto=False).
    """
    if not getattr(user, "is_authenticated", False):
        return None

    # 1) Mapeo explícito
    ue = (UsuarioEmisor.objects
            .filter(user=user)
            .select_related("emisor")
            .order_by("-id")  # si no tienes 'predeterminado', quítalo
            .first())
    if ue and ue.emisor:
        return ue.emisor

    # 2) Perfil con emisor preferido (si lo añadiste)
    emisor_pref = getattr(getattr(user, "perfilusuario", None), "emisor_preferido", None)
    if emisor_pref:
        return emisor_pref

    # 3) Fallback
    if estricto:
        return None
    return Emisor_fe.objects.first()
