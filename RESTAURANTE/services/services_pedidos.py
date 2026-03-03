from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Sum, Min
from RESTAURANTE.models import CuentaPedido, DetallePedido, Pedido
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
    