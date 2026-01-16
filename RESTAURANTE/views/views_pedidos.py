from collections import defaultdict
from datetime import timezone
import json
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import transaction
from FE.models import Receptor_fe
from RESTAURANTE.models import CuentaPedido, DetallePedido, Mesa, Mesero, Pedido, Platillo
from RESTAURANTE.services.services_comandas import enviar_pedido_a_cocina
from RESTAURANTE.services.services_pedidos import split_or_move_detalle


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

def get_or_create_cuenta_default(pedido):
    cuenta = pedido.cuentas.filter(estado="ABIERTA").order_by("creado_el").first()
    if cuenta:
        return cuenta
    return CuentaPedido.objects.create(pedido=pedido, nombre="Cuenta 1", estado="ABIERTA")


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

    cuenta_default = get_or_create_cuenta_default(pedido)
    # Bloquea detalles existentes para evitar carreras
    existentes = {
        str(d.platillo_id): d
        for d in pedido.detalles.select_for_update().filter(cuenta=cuenta_default).select_related("platillo")
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
                cuenta=cuenta_default,
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

    cuenta_default = get_or_create_cuenta_default(pedido)
    detalle = pedido.detalles.filter(platillo=platillo, cuenta=cuenta_default).first()

    if detalle:
        detalle.cantidad += qty
        detalle.save()
    else:
        DetallePedido.objects.create(
            pedido=pedido,
            platillo=platillo,
            cuenta=cuenta_default,
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
@transaction.atomic
def solicitar_cuenta(request, mesa_id):
    print("METHOD >>>> ", request.method)
    """
    Busca el pedido abierto de la mesa y lo cierra
    reutilizando la lógica de pedido_cerrar.
    """
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    # Buscamos el pedido abierto más reciente de esta mesa
    pedido = Pedido.objects.filter(mesa=mesa, estado="ABIERTO").first()

    if not pedido:
        messages.warning(request, f"No se encontró un pedido abierto para la Mesa {mesa.numero}.")
        return redirect("mesas-lista")

    # Llamamos a tu función existente para no repetir lógica
    # Nota: Si pedido_cerrar tiene @require_POST, podrías llamar a pedido.cerrar()
    # directamente aquí para evitar conflictos de método HTTP.
    mesa.estado="PENDIENTE_PAGO"
    mesa.save()
    return pedido_cerrar(request, pedido.id)

@login_required
# @require_POST
@transaction.atomic
def pedido_cerrar(request, pedido_id):
    print("REQUEST METHOD ", request.method)
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")

    mesero = get_mesero_from_user(request.user)
    pedido = get_object_or_404(Pedido.objects.select_for_update(), id=pedido_id)

    if pedido.mesero_id != mesero.id:
        return HttpResponseForbidden("No puedes cerrar este pedido.")

    if pedido.estado != "ABIERTO":
        return HttpResponseBadRequest("El pedido no está ABIERTO.")

    pedido.cerrar()  # cambia a CERRADO y mesa a PENDIENTE_PAGO
    
    
    #TODO: AGREGAR EL TICKET CON EL TOTAL DE LA CUENTA
    
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

@login_required
@transaction.atomic
def pedido_split(request, pedido_id):
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")

    mesero = get_mesero_from_user(request.user)

    pedido = get_object_or_404(
        Pedido.objects.select_for_update(),
        id=pedido_id,
        mesero=mesero,
    )

    cuentas = list(pedido.cuentas.all().order_by("creado_el"))
    cuenta_base = cuentas[0]

    detalles = (
        pedido.detalles
        .select_related("platillo", "cuenta")
        .all()
    )

    from collections import defaultdict
    import json

    def key_of(d):
        return (
            d.platillo_id,
            str(d.precio_unitario),
            str(d.descuento_pct),
            str(int(d.aplica_iva)),
            d.notas or "",
        )

    def key_str(d):
        return f"{d.platillo_id}|{d.precio_unitario}|{d.descuento_pct}|{int(d.aplica_iva)}|{d.notas or ''}"

    items_map = {}

    for d in detalles:
        k = key_of(d)
        if k not in items_map:
            items_map[k] = {
                "platillo": d.platillo,
                "precio": d.precio_unitario,
                "notas": d.notas,
                "por_cuenta": defaultdict(lambda: {"qty": 0, "detalle_id": None}),
            }

        items_map[k]["por_cuenta"][d.cuenta_id]["qty"] += d.cantidad
        items_map[k]["por_cuenta"][d.cuenta_id]["detalle_id"] = d.id

    items = []
    for v in items_map.values():
        v["map_json"] = json.dumps({
            str(cid): {
                "qty": data["qty"],
                "detalle_id": data["detalle_id"],
            }
            for cid, data in v["por_cuenta"].items()
        })
        items.append(v)

    return render(request, "pedidos/split_tabs.html", {
        "pedido": pedido,
        "cuentas": cuentas,
        "cuenta_base": cuenta_base,
        "items": items,
    })
    
@login_required
def enviar_facturacion(request, pedido_id): # <-- Cambiado a pedido_id para coincidir con la URL
    # Si lo que recibes es el ID del pedido, busca el pedido primero
        
    print(f"DEBUG: Intentando facturar Pedido ID: {pedido_id}")
    try:
        pedido = Pedido.objects.get(id=pedido_id)
    except Pedido.DoesNotExist:
        # En lugar de un 404 seco, damos un mensaje amigable
        messages.error(request, f"El pedido #{pedido_id} no existe en el sistema.")
        return redirect('mesas-lista') # O la vista principal de restaurante
    
    # Si necesitas la cuenta, búscala a través del pedido
    cuenta = pedido.cuentas.first() 
    print(f"DEBUG: Intentando facturar cuenta ID: {cuenta}")
    
    if not cuenta:
        messages.error(request, "El pedido no tiene una cuenta asociada.")
        return redirect('pedido-detalle', pedido_id=pedido.id)

    # Buscar al receptor "Clientes Varios"
    receptor = Receptor_fe.objects.filter(num_documento="00000000-0").first()
    
    if not receptor:
        messages.error(request, "No se encontró el receptor por defecto (00000000-0).")
        return redirect('pedido-detalle', pedido_id=pedido.id)

    items = []
    # Usamos los detalles del PEDIDO (o de la cuenta, según tu lógica)
    for detalle in pedido.detalles.all():
        items.append({
            "id": detalle.platillo.producto_id,
            "codigo": getattr(detalle.platillo, 'codigo', 'SERV'),
            "nombre": detalle.platillo.nombre,
            "precio": float(detalle.precio_unitario),
            "cantidad": int(detalle.cantidad),
            "desc_pct": 0.0,
            "iva_on": True,
            "stock": 999 
        })

    request.session["facturacion_prefill"] = {
        "receptor_id": receptor.id,
        "items": items,
        "origen": "restaurante",
        "pedido_id": pedido.id
    }
    request.session.modified = True

    return redirect("/fe/generar/?from_cart=1&restaurante=1")

@login_required
@transaction.atomic
def cuenta_pagar(request, cuenta_id):
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")
    mesero = get_mesero_from_user(request.user)

    cuenta = get_object_or_404(
        CuentaPedido.objects.select_for_update().select_related("pedido", "pedido__mesa"),
        id=cuenta_id,
        pedido__mesero=mesero,
    )
    pedido = cuenta.pedido

    if pedido.estado != "CERRADO":
        messages.error(request, "El pedido debe estar CERRADO para cobrar.")
        return redirect("mesas-lista")

    if cuenta.estado not in ("ABIERTA", "CERRADA"):
        messages.error(request, "Esta cuenta no está disponible para cobro.")
        return redirect("pedido-checkout", pedido.mesa_id)

    # Aquí renderizas form de pago y al POST:
    if request.method == "POST":
        # TODO: aquí registras caja, formas de pago, etc.
        cuenta.estado = "PAGADA"
        cuenta.pagado_el = timezone.now()
        cuenta.save(update_fields=["estado", "pagado_el"])

        # Si todas las cuentas están pagadas → pedido PAGADO y mesa libre
        if not pedido.cuentas.exclude(estado="PAGADA").exists():
            pedido.estado = "PAGADO"
            pedido.pagado_el = timezone.now()
            pedido.save(update_fields=["estado", "pagado_el"])
            pedido._sync_estado_mesa()  # libera mesa

        messages.success(request, f"{cuenta.nombre} pagada.")
        return redirect("pedido-checkout", pedido.mesa_id)

    return render(request, "pedidos/pagar_cuenta.html", {"cuenta": cuenta, "pedido": pedido})

# Seleccionar pago en una sola cuenta o cuentas separadas y añadir cuenta predeterminada (una sola cuenta)
@login_required
@transaction.atomic
def pedido_checkout(request, mesa_id):
   
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")

    mesero = get_mesero_from_user(request.user)
    if not mesero:
        messages.error(request, "No tienes mesero asociado o estás inactivo.")
        return redirect("mesas-lista")

    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    print("MESA ", mesa)
    print("mesero ", mesero)

    pedido = (
        Pedido.objects
        .select_for_update()
        .filter(mesa=mesa, mesero=mesero)
        .order_by("-creado_el")
        .first()
    )
    
    print("pedido ", pedido)
    
    if not pedido:
        print(request, "No hay pedido pendiente de pago en esa mesa.")
        return redirect("mesas-lista")

    # Asegurar cuenta 1 y que todos los detalles tengan cuenta (por si vienen de datos viejos)
    cuenta_default = get_or_create_cuenta_default(pedido)
    pedido.detalles.filter(cuenta__isnull=True).update(cuenta=cuenta_default)

    # Recalcular totales del pedido y de cuentas (opcional, pero recomendado)
    pedido.recalcular_totales(save=True)
    for c in pedido.cuentas.all():
        # si ya agregaste recalcular_totales en CuentaPedido
        try:
            c.recalcular_totales(save=True)
        except Exception:
            pass

    cuentas = pedido.cuentas.all().order_by("creado_el")

    return render(request, "pedidos/checkout.html", {
        "mesa": mesa,
        "pedido": pedido,
        "cuentas": cuentas,
    })

# Agregar mas cuentas en la division de cuentas
@login_required
@require_POST
@transaction.atomic
def crear_cuenta_extra(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Contamos cuántas cuentas existen para ponerle nombre "Cuenta 2", "Cuenta 3", etc.
    num_cuentas = pedido.cuentas.count() + 1
    
    CuentaPedido.objects.create(
        pedido=pedido,
        nombre=f"Cuenta {num_cuentas}",
        estado="ABIERTA"
    )
    
    messages.success(request, f"Cuenta {num_cuentas} creada.")
    return redirect("pedido-split", pedido_id=pedido.id)

@login_required
@require_POST
@transaction.atomic
def detalle_mover_a_cuenta(request):
    print(">>>>>>>>>>> request.method", request.method)
    print(">>>>>>>>>>> request", request)
    
    if getattr(request.user, "role", None) != "mesero":
        return JsonResponse({"ok": False, "error": "Solo meseros."}, status=403)

    mesero = get_mesero_from_user(request.user)

    try:
        detalle_id = int(request.POST["detalle_id"])
        print(">>>>>>>>>>> detalle_id", detalle_id)
        
        cuenta_destino_id = int(request.POST["cuenta_destino_id"])
        print(">>>>>>>>>>> cuenta_destino_id", cuenta_destino_id)
        
        qty = int(request.POST.get("qty") or "1")
        print(">>>>>>>>>>> qty", qty)
        
    except Exception as e:
        print(">>>>>>>>>>> ERROR split_or_move_detalle:", repr(e))
        return JsonResponse({"ok": False, "error": str(e)}, status=400)

    # Validar que el detalle pertenece a un pedido del mesero
    if not DetallePedido.objects.filter(id=detalle_id, pedido__mesero=mesero).exists():
        print(">>>>>>>>>>> exp 1")
        
        return JsonResponse({"ok": False, "error": "No autorizado."}, status=403)

    try:
        print(">>>>>>>>>>> exp 2")
        res = split_or_move_detalle(detalle_id=detalle_id, cuenta_destino_id=cuenta_destino_id, qty=qty)
    except Exception as e:
        print(">>>>>>>>>>> ERROR split_or_move_detalle:", type(e), repr(e))
        return JsonResponse({"ok": False, "error": str(e)}, status=400)


    return JsonResponse({"ok": True, **res})

# Cerrar cuenta
@login_required
@require_POST
@transaction.atomic
def confirmar_division(request, pedido_id):
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")

    mesero = get_mesero_from_user(request.user)
    pedido = get_object_or_404(Pedido.objects.select_for_update(), id=pedido_id, mesero=mesero, estado="CERRADO")

    # (Opcional) evita cuentas vacías
    if pedido.cuentas.filter(detalles__isnull=True).exists():
        messages.error(request, "Hay cuentas vacías. Elimínalas o asigna productos.")
        return redirect("pedido-split", pedido_id=pedido.id)

    pedido.division_confirmada = True
    pedido.save(update_fields=["division_confirmada"])

    pedido.cuentas.filter(estado="ABIERTA").update(estado="CERRADA")
    messages.success(request, "División confirmada. Ya puedes facturar por cuenta.")
    return redirect("pedido-checkout", mesa_id=pedido.mesa_id)

# Enviar cuenta deparada a facturacion
@login_required
@transaction.atomic
def enviar_facturacion_cuenta(request, cuenta_id):
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")
    mesero = get_mesero_from_user(request.user)

    cuenta = get_object_or_404(
        CuentaPedido.objects.select_for_update().select_related("pedido"),
        id=cuenta_id,
        pedido__mesero=mesero,
    )
    pedido = cuenta.pedido

    if pedido.estado != "CERRADO":
        messages.error(request, "El pedido debe estar CERRADO para facturar.")
        return redirect("mesas-lista")

    # si es split confirmado, exigimos CERRADA
    if pedido.division_confirmada and cuenta.estado != "CERRADA":
        messages.error(request, "La cuenta debe estar CERRADA (confirmada) para facturar.")
        return redirect("pedido-checkout", mesa_id=pedido.mesa_id)

    receptor = Receptor_fe.objects.filter(num_documento="00000000-0").first()
    if not receptor:
        messages.error(request, "No se encontró receptor por defecto (00000000-0).")
        return redirect("pedido-checkout", mesa_id=pedido.mesa_id)

    items = []
    for detalle in cuenta.detalles.select_related("platillo").all():
        items.append({
            "id": detalle.platillo.producto_id,
            "codigo": getattr(detalle.platillo, 'codigo', 'SERV'),
            "nombre": detalle.platillo.nombre,
            "precio": float(detalle.precio_unitario),
            "cantidad": int(detalle.cantidad),
            "desc_pct": float(detalle.descuento_pct or 0),
            "iva_on": bool(detalle.aplica_iva),
            "stock": 999,
        })

    request.session["facturacion_prefill"] = {
        "receptor_id": receptor.id,
        "items": items,
        "origen": "restaurante",
        "pedido_id": pedido.id,
        "cuenta_id": cuenta.id,
    }
    request.session.modified = True
    return redirect("/fe/generar/?from_cart=1&restaurante=1")

