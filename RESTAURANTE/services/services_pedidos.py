from django.db import transaction
from django.db.models import Sum, Min

from RESTAURANTE.models import CuentaPedido, DetallePedido

def _assert_cuenta_abierta(cuenta: CuentaPedido):
    if cuenta.estado != "ABIERTA":
        raise ValueError("La cuenta debe estar ABIERTA para poder modificarla.")

def build_map_for_signature(*, pedido_id, platillo_id, precio_unitario, descuento_pct, aplica_iva, notas):
    qs = (DetallePedido.objects
          .filter(
              pedido_id=pedido_id,
              platillo_id=platillo_id,
              precio_unitario=precio_unitario,
              descuento_pct=descuento_pct,
              aplica_iva=aplica_iva,
              notas=notas,
          )
          .values("cuenta_id")
          .annotate(qty=Sum("cantidad"), detalle_id=Min("id")))

    out = {}
    for r in qs:
        cid = str(r["cuenta_id"])
        out[cid] = {"qty": int(r["qty"] or 0), "detalle_id": int(r["detalle_id"]) if r["detalle_id"] else None}
    return out


@transaction.atomic
def split_or_move_detalle(*, detalle_id: int, cuenta_destino_id: int, qty: int):
    det = (DetallePedido.objects.select_for_update().get(id=detalle_id))

    sig = dict(
        pedido_id=det.pedido_id,
        platillo_id=det.platillo_id,
        precio_unitario=det.precio_unitario,
        descuento_pct=det.descuento_pct,
        aplica_iva=det.aplica_iva,
        notas=det.notas,
    )

    if det.cuenta_id == cuenta_destino_id:
        raise ValueError("El detalle ya está en esa cuenta.")

    cuenta_destino = (CuentaPedido.objects.select_for_update()
                      .get(id=cuenta_destino_id, pedido_id=det.pedido_id))

    if det.cuenta is None:
        raise ValueError("El detalle no tiene cuenta origen asignada.")
    if det.cuenta.estado != "ABIERTA" or cuenta_destino.estado != "ABIERTA":
        raise ValueError("Solo se puede mover entre cuentas ABIERTAS.")
    if qty > det.cantidad:
        raise ValueError("No puedes mover más de la cantidad disponible.")

    # MOVE ALL
    if qty == det.cantidad:
        det.cuenta = cuenta_destino
        det.save(update_fields=["cuenta"])

        det.pedido.recalcular_totales(save=True)
        det.cuenta.recalcular_totales(save=True)
        cuenta_destino.recalcular_totales(save=True)

        return {
            "moved_all": True,
            "detalle_origen_id": None,
            "detalle_destino_id": det.id,
            "map": build_map_for_signature(**sig),  # 👈 SIEMPRE
        }

    # PARTIAL
    det.cantidad = det.cantidad - qty
    det.save(update_fields=["cantidad"])

    det_dest = (DetallePedido.objects
        .filter(
            pedido_id=det.pedido_id,
            cuenta_id=cuenta_destino_id,
            platillo_id=det.platillo_id,
            precio_unitario=det.precio_unitario,
            descuento_pct=det.descuento_pct,
            aplica_iva=det.aplica_iva,
            notas=det.notas,
        )
        .select_for_update().first()
    )

    if det_dest:
        det_dest.cantidad = det_dest.cantidad + qty
        det_dest.save(update_fields=["cantidad"])
    else:
        det_dest = DetallePedido.objects.create(
            pedido_id=det.pedido_id,
            cuenta_id=cuenta_destino_id,
            platillo_id=det.platillo_id,
            cantidad=qty,
            precio_unitario=det.precio_unitario,
            descuento_pct=det.descuento_pct,
            aplica_iva=det.aplica_iva,
            notas=det.notas,
        )

    det.pedido.recalcular_totales(save=True)
    det.cuenta.recalcular_totales(save=True)
    cuenta_destino.recalcular_totales(save=True)

    return {
        "moved_all": False,
        "detalle_origen_id": det.id,
        "detalle_destino_id": det_dest.id,
        "map": build_map_for_signature(**sig),  # 👈 SIEMPRE
    }
