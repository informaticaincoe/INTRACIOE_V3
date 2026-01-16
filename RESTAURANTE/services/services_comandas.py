from datetime import timezone
from django.db import transaction
from django.db.models import Sum
from RESTAURANTE.models import Comanda, ComandaItem, DetallePedido, Pedido
from RESTAURANTE.realtime import broadcast_comanda_created

@transaction.atomic
def enviar_pedido_a_cocina(pedido, *, notas=""):
    """
    Crea una Comanda por pedido y crea ComandaItems SOLO por cantidad pendiente.

    Pendiente = detalle.cantidad - sum(comanda_items.cantidad) (excluyendo CANCELADO)
    """
    detalles = (
        DetallePedido.objects
        .select_for_update()
        .filter(pedido=pedido)
        .select_related("platillo")
        .order_by("id")
    )
    
    print(">>>>>>detalles pedido: ", detalles)

    comanda = Comanda.crear_para_pedido(pedido, notas=notas)
    print(">>>>>>dcomanda: ", comanda)

    creados = 0
    for det in detalles:
        enviados = (
            det.comanda_items
            .aggregate(s=Sum("cantidad"))
            .get("s") or 0
        )
        pendiente = int(det.cantidad or 0) - int(enviados)

        if pendiente > 0:
            ComandaItem.objects.create(
                comanda=comanda,
                detalle_pedido=det,
                nombre=det.platillo.nombre,
                cantidad=pendiente,
                notas=(det.notas or "")
            )
            creados += 1

    # si no hubo nada nuevo, no creamos comanda “vacía”
    if creados == 0:
        comanda.delete()
        return None

    transaction.on_commit(lambda: broadcast_comanda_created(comanda))
    return comanda

@transaction.atomic
def marcar_pedido_entregado_por_mesa(mesa, *, usuario):
    """
    Cuando una mesa pasa a ENTREGADO:
    - valida que el pedido ABIERTO exista
    - opcional: bloquea si hay items aún no LISTO
    - pasa items LISTO -> ENTREGADO
    - cierra comandas relacionadas si ya no queda nada pendiente
    """
    pedido = (
        Pedido.objects
        .select_for_update()
        .filter(mesa=mesa, estado="ABIERTO")
        .order_by("-creado_el")
        .first()
    )
    if not pedido:
        return (False, "No hay pedido ABIERTO para esta mesa.")

    # no permitir ENTREGADO si hay items en cocina
    hay_pendientes = ComandaItem.objects.filter(
        comanda__pedido=pedido
    ).exclude(
        estado__in=["LISTO", "ENTREGADO", "CANCELADO"]
    ).exists()

    if hay_pendientes:
        return (False, "Aún hay items en cocina. No puedes marcar la mesa como ENTREGADO.")

    # ✅ marcar items LISTO -> ENTREGADO
    now = timezone.now()
    ComandaItem.objects.filter(
        comanda__pedido=pedido,
        estado="LISTO",
    ).update(
        estado="ENTREGADO",
        entregado_el=now,
        entregado_por=usuario,
    )

    # ✅ cerrar comandas que ya no tengan items pendientes
    comandas = Comanda.objects.select_for_update().filter(pedido=pedido).exclude(estado__in=["ANULADA"])
    for c in comandas:
        # si todos (no cancelados) están ENTREGADO -> CERRADA
        pendientes = c.items.exclude(estado__in=["ENTREGADO", "CANCELADO"]).exists()
        if not pendientes and c.estado != "CERRADA":
            c.estado = "CERRADA"
            if not c.cerrada_el:
                c.cerrada_el = now
            c.save(update_fields=["estado", "cerrada_el"])

    return (True, "Mesa marcada como ENTREGADO y comandas cerradas.")