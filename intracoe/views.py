from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from AUTENTICACION.models import Perfilusuario


@login_required
def index(request):
    # Aquí puedes pasar datos al contexto si es necesario
    #el usuario altual
    


    context = {
        'mensaje': 'Bienvenido a la página principal'
    }
    return render(request, 'base.html', context)