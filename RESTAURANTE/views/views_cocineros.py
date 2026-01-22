from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login

from RESTAURANTE.formsLogin import CocineroLoginForm
from RESTAURANTE.models import AreaCocina, Cocinero


def login_cocinero(request):
    """
    Login de cocineros por PIN (sin contraseña)
    """
    if request.method == "POST":
        form = CocineroLoginForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data["pin"]
            user = authenticate(request, pin=pin)  # autenticación por PIN
            if user:
                login(request, user)
                return redirect("comanda-cocina")
            form.add_error("pin", "PIN inválido o cocinero inactivo.")
    else:
        form = CocineroLoginForm()

    return render(request, "cocina/login_cocinero.html", {"form": form})


def listar_cocineros(request):
    search_query = request.GET.get("search_name")

    # Siempre definir las variables
    cocineros = Cocinero.objects.all().order_by("pk")
    areas_cocina_lista = AreaCocina.objects.all()

    if search_query:
        cocineros = cocineros.filter(nombre__icontains=search_query)

    print("LISTA AREAS ", areas_cocina_lista)
    context = {
        "lista_cocineros": cocineros,
        "lista_areas": areas_cocina_lista
    }

    return render(request, "cocina/cocineros.html", context)

def crear_cocinero(request):
    if request.method == "POST":
        nombre = (request.POST.get("nombre") or "").strip()
        pin = (request.POST.get("pin") or "").strip()
        area_cocina = (request.POST.get("area_cocina") or "").strip()
        activo = request.POST.get("activo") == "on"

        if nombre and pin:
            if Cocinero.objects.filter(pin=pin).exists():
                messages.error(request, "Ya existe un cocinero con ese PIN.")
            else:
                Cocinero.objects.create(nombre=nombre, pin=pin, activo=activo, area_cocina=area_cocina )
                messages.success(request, "Cocinero creado con éxito.")
            return redirect("cocineros-lista")

        messages.error(request, "El nombre y el PIN no pueden estar vacíos.")
        return redirect("cocineros-lista")
    
    areas_cocina_lista = AreaCocina.objects.all()
    context = {
        "lista_areas": areas_cocina_lista
    }

    return render(request, "cocina/formulario_cocinero.html", context)


def editar_cocinero(request, pk):
    cocinero = get_object_or_404(Cocinero, pk=pk)
    areas_cocina_lista = AreaCocina.objects.all()
    
    if request.method == "POST":
        nombre = (request.POST.get("nombre") or "").strip()
        pin = (request.POST.get("pin") or "").strip()
        activo = request.POST.get("activo") == "on"
        area_cocina_id = request.POST.get("area_cocina")

        if not (nombre and pin):
            messages.error(request, "El nombre y el PIN no pueden estar vacíos.")
            return redirect("cocineros-lista")

        # validar PIN único (excluyendo el actual)
        if Cocinero.objects.filter(pin=pin).exclude(pk=cocinero.pk).exists():
            messages.error(request, "Ese PIN ya está en uso por otro cocinero.")
            return redirect("editar-cocinero", pk=cocinero.pk)

        cocinero.nombre = nombre
        cocinero.pin = pin
        cocinero.activo = activo
        cocinero.area_cocina_id = area_cocina_id
        cocinero.save()

        return redirect("cocineros-lista")

    context = {
        "lista_areas": areas_cocina_lista,
        "cocinero": cocinero
    }

    messages.success(request, "Cocinero actualizado con éxito.")

    return render(request, "cocina/formulario_cocinero.html", context)


def eliminar_cocinero(request, pk):
    if request.method == "POST":
        cocinero = get_object_or_404(Cocinero, pk=pk)
        nombre = cocinero.nombre
        cocinero.delete()
        messages.success(request, f'Cocinero "{nombre}" eliminado correctamente.')

    return redirect("cocineros-lista")
