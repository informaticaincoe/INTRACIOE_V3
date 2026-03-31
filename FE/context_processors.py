# FE/context_processors.py
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import ObjectDoesNotExist
from FE.models import Emisor_fe


def emisor_context(request):
    emisor = None
    plan = None
    plan_funcs = set()
    suscripcion_gracia = False
    suscripcion_gracia_fin = None

    try:
        emisor = Emisor_fe.objects.first()
        if emisor and request.user.is_authenticated:
            try:
                suscripcion = emisor.suscripcion
            except ObjectDoesNotExist:
                suscripcion = None

            if suscripcion and suscripcion.esta_vigente():
                plan = suscripcion.plan
                if suscripcion.en_periodo_gracia():
                    suscripcion_gracia = True
                    suscripcion_gracia_fin = suscripcion.gracia_fin
    except (OperationalError, ProgrammingError):
        pass

    # Conjunto de claves de funcionalidades activas para lookup rápido en templates
    if plan:
        try:
            plan_funcs = set(plan.funcionalidades.values_list('clave', flat=True))
        except (OperationalError, ProgrammingError):
            pass

    # Admin y superusuario ven todas las funcionalidades
    if request.user.is_authenticated:
        user_role = getattr(request.user, 'role', '')
        if request.user.is_superuser or user_role == 'admin':
            try:
                from AUTENTICACION.models import Funcionalidad
                plan_funcs = set(Funcionalidad.objects.values_list('clave', flat=True))
            except (OperationalError, ProgrammingError):
                pass

    return {
        "emisor": emisor,
        "plan": plan,
        "plan_funcs": plan_funcs,
        "suscripcion_gracia": suscripcion_gracia,
        "suscripcion_gracia_fin": suscripcion_gracia_fin,
        "modo_demo": emisor.modo_demo if emisor else False,
    }
