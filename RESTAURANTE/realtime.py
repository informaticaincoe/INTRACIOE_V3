from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def broadcast_comanda_created(comanda):
    channel_layer = get_channel_layer()

    area = comanda.area_cocina
    group_name = f"cocina_area_{area.id}"
    print("GROUP_NAME ", group_name)
    
    payload = {
        "id": comanda.id,
        "numero": comanda.numero,
        "estado": comanda.estado,
        "estado_display": comanda.get_estado_display(),
        "mesa_numero": comanda.pedido.mesa.numero,
        "pedido_id": comanda.pedido_id,
        "area_cocina": {
            "id": area.id,
            "nombre": area.area_cocina,
        },
        "items": [
            {
                "id": it.id,
                "cantidad": it.cantidad,
                "nombre": it.nombre,
                "notas": it.notas,
            }
            for it in comanda.items.all()
        ],
    }
    print("PAYLOAD COMANDA ", payload)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "comanda_created",
            "comanda": payload,
        },
    )
    
def broadcast_pedido_listo(*, mesero_user_id: int, mesa_id: int, mesa_numero: int, comanda_id: int):
    try:
        channel_layer = get_channel_layer()
        if not channel_layer:
            return

        data = {
            "mesero_user_id": mesero_user_id,
            "mesa_id": mesa_id,
            "mesa_numero": mesa_numero,
            "comanda_id": comanda_id,
            "mensaje": f"Mesa #{mesa_numero}: pedido listo",
        }

        async_to_sync(channel_layer.group_send)(
            f"mesero_{mesero_user_id}",
            {"type": "pedido_listo", "data": data},
        )
    except Exception:
        print("No se pudo enviar notificación al mesero (Redis/ChannelLayer no disponible).")
        
