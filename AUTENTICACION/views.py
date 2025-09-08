from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Perfilusuario, UsuarioEmisor
from .forms import PerfilUsuarioForm

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