# FE/context_processors.py
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import ObjectDoesNotExist
from FE.models import Emisor_fe  # ajusta según tu modelo real

def emisor_context(request):
    emisor = None

    if not request.user.is_authenticated:
        return {"emisor": emisor}

    try:
        # aquí la lógica que uses para ligar emisor con el usuario/logueado/empresa
        # ejemplo simple:
        emisor = Emisor_fe.objects.first()
    except (OperationalError, ProgrammingError, ObjectDoesNotExist):
        emisor = None

    return {"emisor": emisor}
