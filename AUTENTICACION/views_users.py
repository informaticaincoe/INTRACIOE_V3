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
        username = (request.POST.get("username") or "").strip()
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""
        role = (request.POST.get("role") or "cliente").strip()

        if not username:
            messages.error(request, "El nombre de usuario es obligatorio.")
            return render(request, "autenticacion/usuarios/crear.html")
        if len(username) < 3:
            messages.error(request, "El nombre de usuario debe tener al menos 3 caracteres.")
            return render(request, "autenticacion/usuarios/crear.html")
        if not password or len(password) < 8:
            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")
            return render(request, "autenticacion/usuarios/crear.html")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ya existe un usuario con ese nombre.")
            return render(request, "autenticacion/usuarios/crear.html")

        User.objects.create_user(username=username, email=email, password=password, role=role)
        messages.success(request, "Usuario creado correctamente.")
        return redirect("usuarios_list")

    return render(request, "autenticacion/usuarios/crear.html")

@login_required
def usuarios_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        if not username:
            messages.error(request, "El nombre de usuario es obligatorio.")
            return render(request, "autenticacion/usuarios/editar.html", {"usuario": usuario})
        if len(username) < 3:
            messages.error(request, "El nombre de usuario debe tener al menos 3 caracteres.")
            return render(request, "autenticacion/usuarios/editar.html", {"usuario": usuario})

        usuario.username = username
        usuario.email = (request.POST.get("email") or "").strip()
        usuario.role = (request.POST.get("role") or usuario.role).strip()
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
