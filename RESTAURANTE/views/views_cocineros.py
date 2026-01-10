from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login

from RESTAURANTE.formsLogin import CocineroLoginForm
from RESTAURANTE.models import Cocinero


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
                # cambia este redirect al módulo/pantalla de cocina que tengas
                return redirect("comanda-cocina")
            form.add_error("pin", "PIN inválido o cocinero inactivo.")
    else:
        form = CocineroLoginForm()

    return render(request, "cocina/login_cocinero.html", {"form": form})


def listar_cocineros(request):
    search_query = request.GET.get("search_name")
    if search_query:
        cocineros = Cocinero.objects.filter(nombre__icontains=search_query).order_by("pk")
    else:
        cocineros = Cocinero.objects.all()
    
    print(">>>>>>>>> Cocineros: ", cocineros)

    return render(request, "cocina/cocineros.html", {"lista_cocineros": cocineros})


def crear_cocinero(request):
    if request.method == "POST":
        nombre = (request.POST.get("nombre") or "").strip()
        pin = (request.POST.get("pin") or "").strip()
        activo = request.POST.get("activo") == "on"

        if nombre and pin:
            if Cocinero.objects.filter(pin=pin).exists():
                messages.error(request, "Ya existe un cocinero con ese PIN.")
            else:
                Cocinero.objects.create(nombre=nombre, pin=pin, activo=activo)
                messages.success(request, "Cocinero creado con éxito.")
            return redirect("cocineros-lista")

        messages.error(request, "El nombre y el PIN no pueden estar vacíos.")
        return redirect("cocineros-lista")

    return render(request, "cocina/formulario_cocinero.html")


def editar_cocinero(request, pk):
    cocinero = get_object_or_404(Cocinero, pk=pk)

    if request.method == "POST":
        nombre = (request.POST.get("nombre") or "").strip()
        pin = (request.POST.get("pin") or "").strip()
        activo = request.POST.get("activo") == "on"

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
        cocinero.save()

        messages.success(request, "Cocinero actualizado con éxito.")
        return redirect("cocineros-lista")

    return render(request, "cocina/formulario_cocinero.html", {"cocinero": cocinero})


def eliminar_cocinero(request, pk):
    if request.method == "POST":
        cocinero = get_object_or_404(Cocinero, pk=pk)
        nombre = cocinero.nombre
        cocinero.delete()
        messages.success(request, f'Cocinero "{nombre}" eliminado correctamente.')

    return redirect("cocineros-lista")
