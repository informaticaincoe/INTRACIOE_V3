from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from RESTAURANTE.models import Comanda
from RESTAURANTE.realtime import broadcast_pedido_listo

@login_required
def comanda_cocina(request):
    print("REQUEST ROLE ", request.user.role)
    if request.user.role not in ("cocinero", "admin", "supervisor"):
        return HttpResponseForbidden("No autorizado.")
        

    if request.user.role == "cocinero": #Si es cocinero mostrar solo las comandas de su area
        cocinero = request.user.cocinero
        
        comandas = (
            Comanda.objects
                .filter(
                    area_cocina=cocinero.area_cocina
                )
                .select_related("pedido", "pedido__mesa")
                .prefetch_related("items")
                .exclude(estado__in=["CERRADA", "ANULADA"])
                .order_by("-creada_el")
        )

        return render(
            request,
            "cocina/comanda.html",
            {"comandas": comandas}
        )    
    else: # si es administrador mostrar todas para temas de administracion
        comandas = (
            Comanda.objects.all().order_by("-creada_el")
        )

        return render(
            request,
            "cocina/comanda.html",
            {"comandas": comandas}
        ) 

    

@login_required
@require_POST
@transaction.atomic
def comanda_en_preparacion(request, id):
    if getattr(request.user, "role", None) not in ("cocinero"):
        return HttpResponseForbidden("No autorizado.")

    comanda = get_object_or_404(Comanda.objects.select_for_update(), id=id)
    comanda.estado = "EN_PREPARACION"
    comanda.save()
    
    return JsonResponse({"ok": True})

@login_required
@require_POST
@transaction.atomic
def comanda_listo(request, id):
    if getattr(request.user, "role", None) not in ("cocinero"):
        return HttpResponseForbidden("No autorizado.")

    comanda = get_object_or_404(Comanda.objects.select_for_update(), id=id)
    comanda.estado = "CERRADA"
    comanda.save()
    
    # Datos para notificar
    pedido = comanda.pedido
    mesa = pedido.mesa

    mesero_user_id = pedido.mesero.usuario_id

    print("mesero_user_id: ", mesero_user_id)
    transaction.on_commit(lambda: broadcast_pedido_listo(
        mesero_user_id=mesero_user_id,
        mesa_id=mesa.id,
        mesa_numero=mesa.numero,
        comanda_id=comanda.id
    ))
    
    return JsonResponse({"ok": True})
