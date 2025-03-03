from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    # Aquí puedes pasar datos al contexto si es necesario
    context = {
        'mensaje': 'Bienvenido a la página principal'
    }
    return render(request, 'base.html', context)