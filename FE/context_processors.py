# FE/context_processors.py
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import ObjectDoesNotExist
from FE.models import Emisor_fe


def emisor_context(request):
    if not request.user.is_authenticated:
        return {"emisor": None, "plan": None, "suscripcion_gracia": False, "suscripcion_gracia_fin": None}

    emisor = None
    plan = None
    suscripcion_gracia = False
    suscripcion_gracia_fin = None

    try:
        emisor = Emisor_fe.objects.first()
        if emisor:
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
    plan_funcs = set()
    if plan:
        try:
            plan_funcs = set(plan.funcionalidades.values_list('clave', flat=True))
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
