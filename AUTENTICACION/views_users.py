from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User

@login_required
def usuarios_list(request):
    usuarios = User.objects.all().order_by("username")
    return render(request, "autenticacion/usuarios/list.html", {"usuarios": usuarios})

@login_required
def usuarios_crear(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST.get("email")
        password = request.POST["password"]
        role = request.POST.get("role", "cliente")

        User.objects.create_user(username=username, email=email, password=password, role=role)
        messages.success(request, "Usuario creado correctamente.")
        return redirect("usuarios_list")

    return render(request, "autenticacion/usuarios/crear.html")

@login_required
def usuarios_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        usuario.username = request.POST["username"]
        usuario.email = request.POST.get("email")
        usuario.role = request.POST.get("role", usuario.role)
        usuario.save()
        messages.success(request, "Usuario actualizado.")
        return redirect("usuarios_list")

    return render(request, "autenticacion/usuarios/editar.html", {"usuario": usuario})

@login_required
def usuarios_eliminar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuario eliminado.")
        return redirect("usuarios_list")

    return render(request, "autenticacion/usuarios/eliminar.html", {"usuario": usuario})
