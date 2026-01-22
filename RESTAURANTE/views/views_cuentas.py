from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from RESTAURANTE.models import CuentaPedido, DetallePedido
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
@require_POST
def cambiar_estado_cuenta(request, cuenta_id, estado):
    cuenta = get_object_or_404(CuentaPedido, pk=cuenta_id)
    cuenta.estado = estado
    cuenta.save(update_fields=["estado"])
    return JsonResponse({"ok": True, "estado": cuenta.estado})
    
    
def _consume_qty(qs, qty):
    """
    Resta `qty` recorriendo varias filas (FIFO por id).
    NO borra (por PROTECT). Si llega a 0, deja cantidad=0.
    """
    remaining = qty
    # bloqueo para concurrencia
    for d in qs.select_for_update().order_by("id"):
        if remaining <= 0:
            break
        if d.cantidad <= 0:
            continue
        take = min(d.cantidad, remaining)
        d.cantidad -= take
        if d.cantidad < 0:
            d.cantidad = 0
        d.save(update_fields=["cantidad"])
        remaining -= take

    if remaining > 0:
        raise ValueError("No hay suficiente disponible para mover.")

def _get_or_create_dest(pedido, platillo, cuenta_destino, src_defaults, *, qty):
    qs = (DetallePedido.objects
          .select_for_update()
          .filter(pedido=pedido, platillo=platillo, cuenta=cuenta_destino)
          .order_by("id"))
    first = qs.first()
    if not first:
        # 👇 antes tenías cantidad=0 -> viola el CHECK
        return DetallePedido.objects.create(
            pedido=pedido, platillo=platillo, cuenta=cuenta_destino,
            cantidad=qty, **src_defaults
        ), True

    # (opcional) consolidar duplicados si existen
    dupes = list(qs[1:])
    if dupes:
        extra = sum(d.cantidad for d in dupes if d.cantidad > 0)
        if extra:
            first.cantidad += extra
            first.save(update_fields=["cantidad"])
        for d in dupes:
            if d.cantidad > 0:
                # aquí todavía no sabemos si puedes poner 0 (ver Fix 2)
                d.cantidad = 0
                d.save(update_fields=["cantidad"])

    return first, False

def _build_item_map(pedido, platillo):
    """
    Devuelve cantidades SUMADAS por cuenta y el detalle_id 'usable'
    (el primero con cantidad>0) para que el frontend pueda mover.
    """
    rows = (DetallePedido.objects
            .filter(pedido=pedido, platillo=platillo, cantidad__gt=0)
            .values("id", "cantidad", "cuenta_id")
            .order_by("id"))

    item_map = {}
    for r in rows:
        key = "POOL" if r["cuenta_id"] is None else str(r["cuenta_id"])
        if key not in item_map:
            item_map[key] = {"qty": 0, "detalle_id": r["id"]}
        item_map[key]["qty"] += r["cantidad"]

    item_map.setdefault("POOL", {"qty": 0, "detalle_id": None})
    return item_map