from datetime import timezone
from django.db import transaction
from django.db.models import Sum, Max
from RESTAURANTE.models import Comanda, ComandaItem, DetallePedido, Pedido
from RESTAURANTE.realtime import broadcast_comanda_created
from collections import defaultdict

@transaction.atomic
def enviar_pedido_a_cocina(pedido, *, notas=""):
    """
    Crea UNA comanda por cada área de cocina involucrada
    y agrega SOLO los items pendientes de esa área.
    """

    detalles = (
        DetallePedido.objects
        .select_for_update()
        .filter(
            pedido=pedido,
            platillo__es_preparado=True,
            platillo__area_cocina__isnull=False
        )
        .select_related("platillo", "platillo__area_cocina")
        .order_by("id")
    )

    detalles_por_area = defaultdict(list)
    for det in detalles:
        detalles_por_area[det.platillo.area_cocina].append(det)

    comandas_creadas = []

    for area, detalles_area in detalles_por_area.items():

        # ¿Ya existe comanda activa para esta área?
        comanda = (
            Comanda.objects
            .select_for_update()
            .filter(
                pedido=pedido,
                area_cocina=area,
                estado__in=["ENVIADA", "EN_PREPARACION"]
            )
            .first()
        )

        if not comanda:
            last_num = (
                Comanda.objects
                .filter(pedido=pedido)
                .aggregate(m=Max("numero"))
                .get("m") or 0
            )

            comanda = Comanda.objects.create(
                pedido=pedido,
                area_cocina=area,
                numero=last_num + 1,
                notas=notas,
            )

        creados = 0

        for det in detalles_area:
            enviados = (
                det.comanda_items
                .filter(comanda__area_cocina=area)
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

        if creados == 0:
            comanda.delete()
            continue

        print("DENTRO ENVIAR PEDIDO COCINA ", comanda)
        transaction.on_commit(
            lambda c=comanda: broadcast_comanda_created(c)
        )

        comandas_creadas.append(comanda)

    return comandas_creadas


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