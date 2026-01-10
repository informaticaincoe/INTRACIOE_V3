import json
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import transaction
from FE.models import Receptor_fe
from RESTAURANTE.models import DetallePedido, Mesa, Mesero, Pedido, Platillo
from RESTAURANTE.services_comandas import enviar_pedido_a_cocina

"""
MANEJO DE:
    - Pedidos
    - Detalle pedidos
"""
###############################################################################################################
#                                                 Pedidos                                                     #
###############################################################################################################
def get_mesero_from_user(user):
    if not user.is_authenticated:
        return None
    return Mesero.objects.filter(usuario=user, activo=True).first()

def guardar_detalles_desde_json(pedido, platillos_json: str, *, modo="set"):
    try:
        items = json.loads(platillos_json or "[]")
    except json.JSONDecodeError:
        items = []

    # Normaliza y combina repetidos
    qty_map = {}  # platillo_id(str) -> qty(int)
    for it in items:
        pid = str(it.get("id") or "")
        if not pid:
            continue
        qty = int(it.get("qty") or 1)
        if qty <= 0:
            continue
        qty_map[pid] = qty_map.get(pid, 0) + qty

    if not qty_map:
        return

    # Trae platillos válidos
    platillos = Platillo.objects.filter(id__in=list(qty_map.keys()), disponible=True)
    platillo_map = {str(p.id): p for p in platillos}

    # Bloquea detalles existentes para evitar carreras
    existentes = {
        str(d.platillo_id): d
        for d in pedido.detalles.select_for_update().select_related("platillo")
    }

    nuevos = []

    for pid, qty in qty_map.items():
        p = platillo_map.get(pid)
        if not p:
            continue

        if pid in existentes:
            d = existentes[pid]
            if modo == "add":
                d.cantidad = (d.cantidad or 0) + qty
            else:
                d.cantidad = qty

            d.precio_unitario = p.precio_venta
            d.aplica_iva = True
            d.save()  # llama _calc() y recalcula pedido (si tu save lo hace)
        else:
            d = DetallePedido(
                pedido=pedido,
                platillo=p,
                cantidad=qty,
                precio_unitario=p.precio_venta,
                aplica_iva=True,
            )
            d._calc()  # como bulk_create NO llama save(), calculamos aquí
            nuevos.append(d)

    if nuevos:
        DetallePedido.objects.bulk_create(nuevos)

    # Recalcular una vez al final (recomendado)
    pedido.recalcular_totales(save=True)
    
@login_required
@transaction.atomic
def tomar_pedido(request, mesa_id):
    print("REQUEST", request.method)
    """
    Crea/reutiliza un Pedido ABIERTO para la mesa.
    - Si mesa está PENDIENTE_ORDEN o OCUPADA: ok
    - Si LIBRE: opcionalmente puedes pasarla a PENDIENTE_ORDEN aquí
    """
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")

    mesero = get_mesero_from_user(request.user)
    if not mesero:
        messages.error(request, "No tienes mesero asociado o estás inactivo.")
        return redirect("mesas-lista")

    mesa = get_object_or_404(Mesa, id=mesa_id)

    # Solo permitir si la mesa es del mesero (si tú tienes esa regla)
    # Aquí lo omitimos para simplificar; tú ya filtras por asignación en listar_mesas.

    # Buscar pedido abierto de esa mesa
    pedido = (
        Pedido.objects
        .select_for_update()
        .filter(mesa=mesa, estado="ABIERTO")
        .order_by("-creado_el")
        .first()
    )

    if not pedido:
        pedido = Pedido.objects.create(mesa=mesa, mesero=mesero, estado="ABIERTO")
        # si estaba PENDIENTE_ORDEN, ok; si estaba LIBRE, la ponemos PENDIENTE_ORDEN por seguridad
        if mesa.estado == "LIBRE":
            mesa.estado = "PENDIENTE_ORDEN"
            mesa.save(update_fields=["estado"])

    # productos del menú
    platillos = Platillo.objects.filter(disponible=True).select_related("categoria").order_by("categoria__nombre", "nombre")
    detalles = pedido.detalles.select_related("platillo").all().order_by("id")

    print("PLATILLOS ", platillos)

    context = {
        "mesa": mesa,
        "pedido": pedido,
        "platillos": platillos,
        "detalles": detalles,
    }
    return render(request, "pedidos/_toma_pedido.html", context)

@login_required
@require_POST
@transaction.atomic
def pedido_agregar_item(request, pedido_id):
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")

    mesero = get_mesero_from_user(request.user)
    if not mesero:
        return JsonResponse({"ok": False, "error": "No tienes mesero asociado."}, status=403)

    pedido = get_object_or_404(Pedido.objects.select_for_update(), id=pedido_id)

    if pedido.estado != "ABIERTO":
        return JsonResponse({"ok": False, "error": "El pedido no está ABIERTO."}, status=400)

    # Seguridad: el mesero solo puede editar sus pedidos
    if pedido.mesero_id != mesero.id:
        return JsonResponse({"ok": False, "error": "No puedes editar este pedido."}, status=403)

    platillo_id = request.POST.get("platillo_id")
    qty = int(request.POST.get("cantidad") or "1")
    qty = max(1, qty)

    platillo = get_object_or_404(Platillo, id=platillo_id, disponible=True)

    # Si ya existe el platillo en el pedido, sumamos cantidad
    detalle = pedido.detalles.filter(platillo=platillo).first()
    if detalle:
        detalle.cantidad += qty
        detalle.save()
    else:
        DetallePedido.objects.create(
            pedido=pedido,
            platillo=platillo,
            cantidad=qty,
            precio_unitario=platillo.precio_venta,
            aplica_iva=True,
        )

    # Si ya hay al menos un detalle, la mesa pasa a OCUPADA
    if pedido.mesa.estado != "OCUPADA":
        pedido.mesa.estado = "OCUPADA"
        pedido.mesa.save(update_fields=["estado"])

    pedido.recalcular_totales(save=True)

    return JsonResponse({
        "ok": True,
        "pedido_id": pedido.id,
        "subtotal": str(pedido.subtotal),
        "iva_total": str(pedido.iva_total),
        "total": str(pedido.total),
    })

@login_required
@require_POST
@transaction.atomic
def pedido_quitar_item(request, pedido_id, detalle_id):
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")

    mesero = get_mesero_from_user(request.user)
    pedido = get_object_or_404(Pedido.objects.select_for_update(), id=pedido_id)
    if pedido.mesero_id != mesero.id:
        return HttpResponseForbidden("No puedes editar este pedido.")

    det = get_object_or_404(DetallePedido, id=detalle_id, pedido=pedido)
    det.delete()

    pedido.recalcular_totales(save=True)

    # si ya no hay items, regresamos a PENDIENTE_ORDEN
    if not pedido.detalles.exists():
        if pedido.mesa.estado != "PENDIENTE_ORDEN":
            pedido.mesa.estado = "PENDIENTE_ORDEN"
            pedido.mesa.save(update_fields=["estado"])

    return JsonResponse({
        "ok": True,
        "subtotal": str(pedido.subtotal),
        "iva_total": str(pedido.iva_total),
        "total": str(pedido.total),
    })

@login_required
@require_POST
@transaction.atomic
def pedido_cerrar(request, pedido_id):
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")

    mesero = get_mesero_from_user(request.user)
    pedido = get_object_or_404(Pedido.objects.select_for_update(), id=pedido_id)

    if pedido.mesero_id != mesero.id:
        return HttpResponseForbidden("No puedes cerrar este pedido.")

    if pedido.estado != "ABIERTO":
        return HttpResponseBadRequest("El pedido no está ABIERTO.")

    pedido.cerrar()  # cambia a CERRADO y mesa a PENDIENTE_PAGO
    messages.success(request, "Pedido enviado a cobro (pendiente de pago).")
    return redirect("mesas-lista")


@login_required
@transaction.atomic
def pedido_crear_desde_mesa(request):
    if request.method == "POST":
        if getattr(request.user, "role", None) != "mesero": # solo los meseros podra realizar toda la ruta de los pedidos
            messages.error(request, "No autorizado.")
            return redirect("mesas-lista")

        mesero = get_mesero_from_user(request.user) # obtener el mesero que esta loggeado
        if not mesero:
            messages.error(request, "No tienes un mesero asociado o estás inactivo.")
            return redirect("mesas-lista")

        # obtener datos para realizar pedido
        mesa_id = request.POST.get("mesa_id") 
        notas = (request.POST.get("notas") or "").strip()
        receptor_id = request.POST.get("receptor_id") or None

        mesa = get_object_or_404(Mesa.objects.select_for_update(), id=mesa_id)

        # Solo permitir si la mesa está pendiente de orden
        if mesa.estado not in ("PENDIENTE_ORDEN", "OCUPADA"):
            messages.error(request, f"No se puede tomar el pedido en una mesa en estado: {mesa.estado}")
            return redirect("mesas-lista")

        # Reusar pedido ABIERTO si existe
        pedido = (
            Pedido.objects
            .select_for_update()
            .filter(mesa=mesa, estado="ABIERTO", mesero=mesero)
            .order_by("-creado_el")
            .first()
        )
        if not pedido:
            pedido = Pedido.objects.create(mesa=mesa, mesero=mesero, estado="ABIERTO")

        # Receptor: si no viene, Clientes Varios
        if receptor_id:
            pedido.receptor = get_object_or_404(Receptor_fe, id=receptor_id)
        if notas:
            pedido.notas = notas

        pedido.save(update_fields=["receptor", "notas"])

        # ✅ GUARDAR DETALLES (lo que se seleccionó en el modal)
        platillos_json = request.POST.get("platillos_json", "[]")
        guardar_detalles_desde_json(pedido, platillos_json, modo="set")  # o modo="add"

        # ✅ Estado de la mesa según si hay items
        if pedido.detalles.exists():
            if mesa.estado != "OCUPADA":
                mesa.estado = "OCUPADA"
                mesa.save(update_fields=["estado"])
        else:
            if mesa.estado != "PENDIENTE_ORDEN":
                mesa.estado = "PENDIENTE_ORDEN"
                mesa.save(update_fields=["estado"])
        
        if pedido.detalles.exists():
            comanda = enviar_pedido_a_cocina(pedido, notas=notas)
            if comanda:
                messages.success(request, f"Pedido enviado a cocina (Comanda #{comanda.numero}).")
            else:
                messages.info(request, "No hay items pendientes por enviar a cocina.")
        else:
            messages.error(request, "No se enviaron items a cocina porque el pedido está vacío.")

        return redirect("mesas-lista")
    
def ver_pedido_mesa(request, pk):    
    mesa = get_object_or_404(Mesa, pk=pk)
    
    mesero = get_mesero_from_user(request.user)
    if getattr(request.user, "role", None) != "mesero" or not mesero:
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=403)

    pedido = (Pedido.objects
              .filter(mesa_id=mesa.id, estado="ABIERTO", mesero=mesero)
              .prefetch_related("detalles__platillo")
              .order_by("-creado_el")
              .first())

    if not pedido:
        return JsonResponse({"ok": False, "error": "No hay pedido abierto"}, status=404)
    
    detalles = []
    for d in pedido.detalles.select_related("platillo").all():
        img = ""
        if d.platillo.imagen:
            img = d.platillo.imagen.url 
        detalles.append({
            "id": d.id,
            "platillo_id": d.platillo_id,
            "nombre": d.platillo.nombre,
            "qty": d.cantidad,
            "precio": float(d.precio_unitario),
            "total": float(d.total_linea),
            "imagen_url": img,
        })

    return JsonResponse({
        "ok": True,
        "pedido": {
            "id": pedido.id,
            "mesa_id": pedido.mesa_id,
            "estado": pedido.estado,
            "notas": pedido.notas,
            "subtotal": float(pedido.subtotal),
            "iva_total": float(pedido.iva_total),
            "total": float(pedido.total),
        },
        "detalles": detalles
    })
    