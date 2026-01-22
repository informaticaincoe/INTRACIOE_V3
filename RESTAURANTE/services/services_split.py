# # services_split.py
# from django.db import transaction
# from decimal import Decimal
# from .models import DetallePedido, CuentaPedido, Pedido

# @transaction.atomic
# def split_or_move_detalle(*, detalle_id: int, cuenta_destino_id: int, qty: int):
#     qty = int(qty)
#     if qty <= 0:
#         raise ValueError("Cantidad inválida.")

#     det = (
#         DetallePedido.objects
#         .select_for_update()
#         .select_related("pedido", "cuenta")
#         .get(id=detalle_id)
#     )

#     pedido = (
#         Pedido.objects
#         .select_for_update()
#         .get(id=det.pedido_id)
#     )

#     if pedido.estado != "CERRADO":
#         raise ValueError("Solo puedes dividir cuando el pedido está CERRADO.")
#     if pedido.division_confirmada:
#         raise ValueError("La división ya fue confirmada, no se puede modificar.")

#     if not det.cuenta_id:
#         raise ValueError("Este detalle no tiene cuenta asignada.")

#     cuenta_dest = (
#         CuentaPedido.objects
#         .select_for_update()
#         .get(id=cuenta_destino_id)
#     )

#     if cuenta_dest.pedido_id != pedido.id:
#         raise ValueError("La cuenta destino no pertenece a este pedido.")
#     if cuenta_dest.estado != "ABIERTA":
#         raise ValueError("La cuenta destino no está ABIERTA.")

#     cuenta_origen = det.cuenta
#     if cuenta_origen.estado != "ABIERTA":
#         raise ValueError("La cuenta origen no está ABIERTA.")
#     if cuenta_origen.id == cuenta_dest.id:
#         return _resumen(pedido)

#     if qty > det.cantidad:
#         raise ValueError("No puedes mover más de la cantidad disponible.")

#     # --- Caso A: mover línea completa ---
#     if qty == det.cantidad:
#         det.cuenta = cuenta_dest
#         det.save(update_fields=["cuenta"])  # save recalcula línea y pedido
#         cuenta_origen.recalcular_totales(save=True)
#         cuenta_dest.recalcular_totales(save=True)
#         pedido.recalcular_totales(save=True)
#         return _resumen(pedido)

#     # --- Caso B: split parcial ---
#     det.cantidad -= qty
#     det.save(update_fields=["cantidad"])  # save recalcula línea y pedido

#     # Buscar si ya existe una línea equivalente en la cuenta destino y sumar
#     det_dest = (
#         DetallePedido.objects
#         .select_for_update()
#         .filter(
#             pedido_id=pedido.id,
#             cuenta_id=cuenta_dest.id,
#             platillo_id=det.platillo_id,
#             precio_unitario=det.precio_unitario,
#             descuento_pct=det.descuento_pct,
#             aplica_iva=det.aplica_iva,
#             notas=det.notas,
#         )
#         .first()
#     )

#     if det_dest:
#         det_dest.cantidad += qty
#         det_dest.save(update_fields=["cantidad"])
#     else:
#         DetallePedido.objects.create(
#             pedido_id=pedido.id,
#             cuenta_id=cuenta_dest.id,
#             platillo_id=det.platillo_id,
#             cantidad=qty,
#             precio_unitario=det.precio_unitario,
#             descuento_pct=det.descuento_pct,
#             aplica_iva=det.aplica_iva,
#             notas=det.notas,
#         )

#     # Recalcular cuentas (pedido ya se recalculó varias veces por tu save(), pero lo dejamos consistente)
#     cuenta_origen.recalcular_totales(save=True)
#     cuenta_dest.recalcular_totales(save=True)
#     pedido.recalcular_totales(save=True)

#     return _resumen(pedido)


# def _resumen(pedido: Pedido):
#     cuentas = pedido.cuentas.all().order_by("creado_el")
#     return {
#         "pedido_total": str(pedido.total),
#         "cuentas": [{"id": c.id, "nombre": c.nombre, "estado": c.estado, "total": str(c.total)} for c in cuentas],
#     }
