from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Sum, Min
from RESTAURANTE.models import CuentaPedido, DetallePedido
from collections import defaultdict
import json

def _assert_cuenta_abierta(cuenta: CuentaPedido):
    if cuenta.estado != "ABIERTA":
        raise ValueError("La cuenta debe estar ABIERTA para poder modificarla.")


def crear_map_json_por_item(item):
    """
    Construye el JSON con cantidades por cuenta y total para un item (dict).
    """
    map_data = {}
    total_qty = 0
    for cuenta_id, data in item["por_cuenta"].items():
        map_data[str(cuenta_id)] = {
            "qty": data["qty"],
            "detalle_id": data["detalle_ids"][0] if data["detalle_ids"] else None,
        }
        total_qty += data["qty"]
    map_data["total_qty"] = total_qty
    return json.dumps(map_data)

# @transaction.atomic
# def split_or_move_detalle(*, detalle_id: int, cuenta_destino_id: int, qty: int):
#     """
#     Mueve un DetallePedido (total o parcial) a una CuentaPedido.
#     Si qty < cantidad actual, divide el detalle.
#     """

#     if qty <= 0:
#         raise ValidationError("La cantidad debe ser mayor a cero.")

#     # 1. Lock del detalle
#     detalle = (
#         DetallePedido.objects
#         .select_for_update()
#         .select_related("pedido", "cuenta")
#         .get(id=detalle_id)
#     )

#     pedido = detalle.pedido

#     if pedido.estado != "CERRADO":
#         raise ValidationError("El pedido debe estar CERRADO para dividir cuentas.")

#     # 2. Cuenta destino
#     cuenta_destino = (
#         CuentaPedido.objects
#         .select_for_update()
#         .get(id=cuenta_destino_id, pedido=pedido)
#     )

#     if cuenta_destino.estado != "ABIERTA":
#         raise ValidationError("La cuenta destino no está ABIERTA.")

#     if qty > detalle.cantidad:
#         raise ValidationError("La cantidad excede la disponible.")

#     # 3. Caso A: mover TODO el detalle
#     if qty == detalle.cantidad:
#         detalle.cuenta = cuenta_destino
#         detalle.save(update_fields=["cuenta"])
#         cuenta_destino.recalcular_totales(save=True)
#         return {
#             "accion": "mover_completo",
#             "detalle_id": detalle.id,
#             "cantidad": qty,
#             "cuenta_id": cuenta_destino.id,
#         }

#     # 4. Caso B: mover PARCIAL (split)
#     # Reducimos el detalle original
#     detalle.cantidad -= qty
#     detalle.save(update_fields=["cantidad"])

#     # Creamos nuevo detalle para la cuenta destino
#     nuevo = DetallePedido.objects.create(
#         pedido=pedido,
#         platillo=detalle.platillo,
#         cuenta=cuenta_destino,
#         cantidad=qty,
#         precio_unitario=detalle.precio_unitario,
#         descuento_pct=detalle.descuento_pct,
#         aplica_iva=detalle.aplica_iva,
#         notas=detalle.notas,
#     )

#     # 5. Recalcular totales
#     cuenta_destino.recalcular_totales(save=True)

#     if detalle.cuenta:
#         detalle.cuenta.recalcular_totales(save=True)

#     pedido.recalcular_totales(save=True)

#     return {
#         "accion": "split",
#         "detalle_origen_id": detalle.id,
#         "detalle_nuevo_id": nuevo.id,
#         "cantidad_movida": qty,
#         "cuenta_id": cuenta_destino.id,
#     }

# CUENTAS -----------------
@transaction.atomic
def pagar_cuenta(*, cuenta_id: int):
    cuenta = CuentaPedido.objects.select_for_update().select_related("pedido").get(id=cuenta_id)

    if cuenta.estado == "PAGADA":
        return

    if cuenta.estado not in ["CERRADA", "ABIERTA"]:
        raise ValueError("La cuenta no se puede pagar en este estado.")

    cuenta.estado = "PAGADA"
    cuenta.pagado_el = timezone.now()
    # cuenta.caja_id = caja_id  # si aplica
    cuenta.save(update_fields=["estado", "pagado_el"])

    # 👇 aquí se hace el cierre agregado
    cuenta.pedido.marcar_pagado_si_corresponde()