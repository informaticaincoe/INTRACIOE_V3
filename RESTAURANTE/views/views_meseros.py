from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from RESTAURANTE.formsLogin import MeseroLoginForm
from RESTAURANTE.models import Mesero

"""
MANEJO DE:
    - Login Meseros
    - Meseros
"""
###############################################################################################################
#                                                 Meseros                                                     #
###############################################################################################################
def login_mesero(request):
    if request.method == "POST":
        form = MeseroLoginForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data["codigo"]
            user = authenticate(request, codigo=codigo)  # autenticacion por codigo
            if user:
                login(request, user)
                return redirect("mesas-lista")
            form.add_error("codigo", "Código inválido o mesero inactivo.")
    else:
        form = MeseroLoginForm()

    return render(request, "loginMeseros/mesero_login.html", {"form": form})


def listar_meseros(request):
    search_query = request.GET.get('search_name')
    if search_query:
        meseros = Mesero.objects.filter(nombre__icontains=search_query) # Filtrar meseros por nombre
    else:
        meseros = Mesero.objects.all().order_by("pk")
    context = {
        'lista_meseros': meseros  # Lista de meseros
    }
    return render(request, 'meseros/meseros.html', context)


def crear_mesero(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre') or ''
        codigo = request.POST.get('codigo') or ''
        activo = request.POST.get('activo') == "on"
        
        if nombre and codigo:
                Mesero.objects.create(
                    nombre = nombre,
                    codigo = codigo,
                    activo=activo,
                )
                messages.success(request, f'Mesero creado con exito.')
        else:
            messages.error(request, 'El nombre y codigo del mesero no pueden estar vacíos.')
            
        # Redirigir después de POST para evitar reenvío del formulario
        return redirect('meseros-lista')
        
    return render(request, 'meseros/formulario.html')

def editar_mesero(request, pk):
    if request.method == "POST":
        nombre = request.POST.get('nombre') or ''
        codigo = request.POST.get('codigo') or ''
        activo = request.POST.get('activo') == "on"
        
        
        if nombre and codigo:
            mesero = get_object_or_404(Mesero, pk=pk)
            mesero.nombre = nombre
            mesero.codigo = codigo            
            mesero.activo = activo
            mesero.save()

            messages.success(request, f'Mesero creado con éxito.')
        else:
            messages.error(request, 'El nombre y codigo del mesero no puede estar vacío.')
            
        # redirigir después de POST para evitar reenvío del formulario
        return redirect('meseros-lista')
   
    mesero = get_object_or_404(Mesero, pk=pk)
    context = {
        "mesero": mesero    
    }
    return render(request, 'meseros/formulario.html', context)

def eliminar_mesero(request, pk):
    print("pk ", pk)
    print("method ", request.method)
    
    if request.method == "POST":
        mesero = get_object_or_404(Mesero, pk=pk)
        mesero_nombre = mesero.nombre
        mesero.delete()
        messages.success(request, f'Mesero "{mesero_nombre}" eliminado correctamente.')
        
    return redirect('meseros-lista')