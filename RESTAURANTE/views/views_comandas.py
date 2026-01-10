from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from RESTAURANTE.models import Comanda, ComandaItem

@login_required
def comanda_cocina(request):
    if getattr(request.user, "role", None) not in ("cocinero", "admin", "supervisor"):
        return HttpResponseForbidden("No autorizado.")

    # Trae comandas activas con sus items (pendientes de cocina)
    comandas = (
        Comanda.objects
        .select_related("pedido", "pedido__mesa")
        .prefetch_related("items")
        .exclude(estado__in=["CERRADA", "ANULADA"])
        .order_by("-creada_el")
    )
    return render(request, "cocina/comanda.html", {"comandas": comandas})

@login_required
@require_POST
@transaction.atomic
def comanda_item_en_preparacion(request, item_id):
    if getattr(request.user, "role", None) not in ("cocinero"):
        return HttpResponseForbidden("No autorizado.")

    item = get_object_or_404(ComandaItem.objects.select_for_update(), id=item_id)
    print("*** item: ", item)
    item.marcar_en_preparacion(request.user)
    print("*** item: ", item)
    
    return JsonResponse({"ok": True})

@login_required
@require_POST
@transaction.atomic
def comanda_item_listo(request, item_id):
    if getattr(request.user, "role", None) not in ("cocinero"):
        return HttpResponseForbidden("No autorizado.")

    item = get_object_or_404(ComandaItem.objects.select_for_update(), id=item_id)
    item.marcar_listo(request.user)
        
    
    
    return JsonResponse({"ok": True})
