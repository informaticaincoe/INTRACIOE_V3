from django.db import transaction

from RESTAURANTE.models import CuentaPedido, DetallePedido

def _assert_cuenta_abierta(cuenta: CuentaPedido):
    if cuenta.estado != "ABIERTA":
        raise ValueError("La cuenta debe estar ABIERTA para poder modificarla.")

@transaction.atomic
def split_or_move_detalle(detalle_id: int, cuenta_destino_id: int, qty: int):
    detalle = (
        DetallePedido.objects
        .select_for_update()
        .select_related("pedido", "cuenta")
        .get(id=detalle_id)
    )
    cuenta_destino = (
        CuentaPedido.objects
        .select_for_update()
        .get(id=cuenta_destino_id)
    )

    if detalle.pedido_id != cuenta_destino.pedido_id:
        raise ValueError("La cuenta destino no pertenece al mismo pedido.")

    if qty <= 0:
        raise ValueError("qty debe ser mayor que 0.")
    if qty > detalle.cantidad:
        raise ValueError("qty no puede ser mayor que la cantidad del detalle.")

    # estados
    if detalle.pedido.estado != "ABIERTO":
        raise ValueError("Solo se puede separar cuentas cuando el pedido está ABIERTO.")
    if detalle.cuenta_id:
        _assert_cuenta_abierta(detalle.cuenta)
    _assert_cuenta_abierta(cuenta_destino)

    cuenta_origen_id = detalle.cuenta_id

    # Si ya está en cocina: no partir parcial (recomendación)
    if qty < detalle.cantidad and detalle.comanda_items.exists():
        raise ValueError("No se puede partir parcialmente un ítem ya enviado a cocina. Mueve el ítem completo o registra ítems separados desde el inicio.")

    # Caso 1: mover todo
    if qty == detalle.cantidad:
        detalle.cuenta = cuenta_destino
        detalle.save(update_fields=["cuenta"], skip_recalc=True)

        # recalcular ambas cuentas + pedido una sola vez
        if cuenta_origen_id:
            CuentaPedido.objects.get(id=cuenta_origen_id).recalcular_totales(save=True)
        cuenta_destino.recalcular_totales(save=True)
        detalle.pedido.recalcular_totales(save=True)

        return {"moved_all": True, "new_detalle_id": None}

    # Caso 2: partir (qty < cantidad)
    # 1) reducir original
    detalle.cantidad = detalle.cantidad - qty
    detalle.save(update_fields=["cantidad"], skip_recalc=True)

    # 2) crear nuevo detalle en cuenta destino (copia de campos)
    nuevo = DetallePedido.objects.create(
        pedido=detalle.pedido,
        cuenta=cuenta_destino,
        platillo=detalle.platillo,
        cantidad=qty,
        precio_unitario=detalle.precio_unitario,
        descuento_pct=detalle.descuento_pct,
        aplica_iva=detalle.aplica_iva,
        notas=detalle.notas,
    )
    # el create llama save() y calcula línea; pero recalcula pedido/cuenta.
    # Para evitar doble recálculo, podés crear con skip_recalc=True así:
    # nuevo = DetallePedido(
    #   ... )
    # nuevo.save(skip_recalc=True)

    # Recalcular (si no usaste skip_recalc en create, igual no pasa nada, solo es más costoso)
    if cuenta_origen_id:
        CuentaPedido.objects.get(id=cuenta_origen_id).recalcular_totales(save=True)
    cuenta_destino.recalcular_totales(save=True)
    detalle.pedido.recalcular_totales(save=True)

    return {"moved_all": False, "new_detalle_id": nuevo.id}
