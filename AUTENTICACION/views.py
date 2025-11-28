from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Perfilusuario, UsuarioEmisor
from .forms import PerfilUsuarioForm

from django.contrib.auth import get_user_model 

User = get_user_model()

@login_required
def perfil_usuario_view(request):
    perfil, _ = Perfilusuario.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PerfilUsuarioForm(request.POST, instance=perfil, user=request.user)
        if form.is_valid():
            nuevo_perfil = form.save(commit=False)
            # Validar que el emisor elegido esté permitido
            emisor_sel = form.cleaned_data.get("emisor_activo")
            if emisor_sel:
                permitido = UsuarioEmisor.objects.filter(
                    user=request.user, emisor=emisor_sel, activo=True
                ).exists() or request.user.is_superuser
                if not permitido:
                    messages.error(request, "No tiene permiso para usar ese emisor.")
                else:
                    nuevo_perfil.emisor_activo = emisor_sel
            nuevo_perfil.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("perfil_usuario")
    else:
        form = PerfilUsuarioForm(instance=perfil, user=request.user)

    # Emisores permitidos, para listarlos (tabla/cards)
    emisores_permitidos = (
        UsuarioEmisor.objects
        .select_related("emisor")
        .filter(user=request.user, activo=True)
        .order_by("-es_predeterminado", "emisor__nombre_razon_social")
    )

    return render(request, "perfil.html", {
        "form": form,
        "perfil": perfil,
        "emisores_permitidos": emisores_permitidos,
    })

def es_admin(user):
    return user.is_authenticated and user.role == "admin"

@login_required
@user_passes_test(es_admin)
def usuarios_list(request):
    usuarios = User.objects.all()
    return render(request, "usuarios/list.html", {"usuarios": usuarios})

@login_required
@user_passes_test(es_admin)
def usuarios_crear(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST["role"]
        user = User.objects.create_user(username=username, password=password, role=role)
        messages.success(request, "Usuario creado correctamente.")
        return redirect("usuarios_list")
    return render(request, "usuarios/crear.html", {"roles": User.ROLE_CHOICES})

@login_required
@user_passes_test(es_admin)
def usuarios_editar(request, pk):
    u = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        u.username = request.POST["username"]
        u.role = request.POST["role"]
        if request.POST.get("password"):
            u.set_password(request.POST["password"])
        u.save()
        messages.success(request, "Usuario actualizado.")
        return redirect("usuarios_list")
    return render(request, "usuarios/editar.html", {"usuario": u, "roles": User.ROLE_CHOICES})

@login_required
@user_passes_test(es_admin)
def usuarios_eliminar(request, pk):
    u = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        u.delete()
        messages.success(request, "Usuario eliminado.")
        return redirect("usuarios_list")
    return render(request, "usuarios/eliminar.html", {"usuario": u})