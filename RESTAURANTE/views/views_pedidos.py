from datetime import timezone
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import transaction
from FE.models import Receptor_fe
from RESTAURANTE.models import Caja, Comanda, CuentaPedido, DetallePedido, Mesa, Mesero, Pedido, Platillo
from RESTAURANTE.services.services_comandas import enviar_pedido_a_cocina
from RESTAURANTE.services.services_pedidos import crear_map_json_por_item
from django.db.models import Sum

from RESTAURANTE.views.views_cuentas import _build_item_map, _consume_qty, _get_or_create_dest

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

# GUARDAR LOS DETALLES DEL PEDIDO
def guardar_detalles_desde_json(pedido, platillos_json: str, *, modo="set"):
    import json

    try:
        items = json.loads(platillos_json or "[]")
    except json.JSONDecodeError:
        items = []

    # 1. Normalizar y combinar repetidos
    qty_map = {}
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

    # 2. Obtener platillos válidos
    platillos = Platillo.objects.filter(
        id__in=list(qty_map.keys()),
        disponible=True
    )
    platillo_map = {str(p.id): p for p in platillos}

    # 3. MODO SET → borrar detalles previos
    if modo == "set":
        pedido.detalles.all().delete()

    nuevos_detalles = []

    for pid, qty in qty_map.items():
        p = platillo_map.get(pid)
        if not p:
            continue

        d = DetallePedido(
            pedido=pedido,
            platillo=p,
            cuenta=None,  # 🔥 CLAVE: sin cuenta
            cantidad=qty,
            precio_unitario=p.precio_venta,
            aplica_iva=True,
        )

        if hasattr(d, "_calc"):
            d._calc()

        nuevos_detalles.append(d)

    # 4. Guardado masivo
    if nuevos_detalles:
        DetallePedido.objects.bulk_create(nuevos_detalles)

    # 5. Recalcular totales del pedido
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

    qty = int(request.POST.get("cantidad") or "1")
    qty = max(1, qty)

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
    if not Caja.objects.filter(estado="ABIERTA").exists():
        messages.error(request, "Denegado: No hay una caja abierta.", extra_tags="error-caja-cerrada")
        return redirect("mesas-lista")
    
    if request.method == "POST":
        mesero = get_mesero_from_user(request.user) # obtener el mesero que esta loggeado
        if not mesero:
            print(request, "No tienes un mesero asociado o estás inactivo.")
            return redirect("mesas-lista")

        mesa_id = request.POST.get("mesa_id") 
        notas = (request.POST.get("notas") or "").strip()
        receptor_id = request.POST.get("receptor_id") or None

        mesa = get_object_or_404(Mesa.objects.select_for_update(), id=mesa_id)

        if mesa.estado not in ("PENDIENTE_ORDEN", "OCUPADA"):
            messages.error(request, f"Estado de mesa no válido: {mesa.estado}")
            return redirect("mesas-lista")

        pedido, created = Pedido.objects.select_for_update().get_or_create(
            mesa=mesa, 
            estado="ABIERTO", 
            mesero=mesero,
            defaults={'estado': 'ABIERTO'}
        )

        if receptor_id:
            pedido.receptor = get_object_or_404(Receptor_fe, id=receptor_id)
        if notas:
            pedido.notas = notas
        pedido.save()

        # ✅ GUARDAR DETALLES
        platillos_json = request.POST.get("platillos_json", "[]")
        print(f"DEBUG: JSON RECIBIDO -> {platillos_json}") # Revisa esto en tu consola
        guardar_detalles_desde_json(pedido, platillos_json, modo="set")

        # 💡 SOLUCIÓN AL PUNTO 1: Refrescar los detalles desde la DB
        # Esto asegura que .exists() sea real
        tiene_detalles = pedido.detalles.all().exists()
        print("TIENE DETALLES ", tiene_detalles)
        if tiene_detalles:
            # ✅ Cambiar estado de la mesa a OCUPADA
            if mesa.estado != "OCUPADA":
                mesa.estado = "OCUPADA"
                mesa.save() # Quitamos update_fields para asegurar el guardado total o verificar signals

            # ✅ ENVIAR A COCINA
            comanda = enviar_pedido_a_cocina(pedido, notas=notas)
            print("comanda ", comanda)
            
            if comanda:
                messages.success(request, f"Pedido enviado a cocina (Comanda).")
            else:
                # Si enviar_pedido_a_cocina devuelve None, revisa esa función. 
                # Puede que esté marcando los items como 'ya enviados'.
                messages.info(request, "El pedido se guardó, pero no había items nuevos para cocina.")
        else:
            # Si el pedido quedó vacío, regresamos la mesa a PENDIENTE_ORDEN
            mesa.estado = "PENDIENTE_ORDEN"
            mesa.save()
            messages.warning(request, "El pedido está vacío.")

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
    # 1. Seguridad
    # if getattr(request.user, "role", None) != "mesero":
    #     return HttpResponseForbidden("Solo meseros.")

    # mesero = get_mesero_from_user(request.user)

    # 2. Pedido con lock
    pedido = get_object_or_404(
        Pedido.objects.select_for_update(),
        id=pedido_id,
        # mesero=mesero,
        estado="CERRADO",  # solo se divide cuando ya pidió la cuenta
    )

    # 3. Cuentas existentes (puede no haber ninguna aún)
    cuentas = list(pedido.cuentas.all().order_by("creado_el"))

    # 4. Detalles del pedido
    detalles = (
        pedido.detalles
        .select_related("platillo", "cuenta")
        .all()
    )

    from collections import defaultdict

    def key_of(d):
        """
        Agrupa líneas equivalentes:
        mismo platillo, precio, descuento, iva y notas
        """
        return (
            d.platillo_id,
            str(d.precio_unitario),
            str(d.descuento_pct),
            str(int(d.aplica_iva)),
            d.notas or "",
        )

    items_map = {}

    for d in detalles:
        k = key_of(d)

        if k not in items_map:
            items_map[k] = {
                "platillo": d.platillo,
                "precio": d.precio_unitario,
                "notas": d.notas,
                "por_cuenta": defaultdict(lambda: {
                    "qty": 0,
                    "detalle_ids": []
                }),
            }

        cuenta_key = d.cuenta_id or "POOL"  # POOL = sin asignar
        items_map[k]["por_cuenta"][cuenta_key]["qty"] += d.cantidad
        items_map[k]["por_cuenta"][cuenta_key]["detalle_ids"].append(d.id)

    # 5. Preparar items para la UI
    items = []
    for item in items_map.values():
        platillo_obj = item["platillo"]
        map_json = crear_map_json_por_item(item)
        items.append({
            "platillo": platillo_obj,
            "cantidad": sum(data["qty"] for data in item["por_cuenta"].values()),
            "precio": item["precio"],
            "map_json": map_json,
        })
    
    context = {
        "pedido": pedido,
        "cuentas": cuentas,
        "items": items,
    }
    # 6. Render
    return render(request, "pedidos/split_tabs.html", context)

    
@login_required
def enviar_facturacion(request, pedido_id, cuenta_id=None):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if cuenta_id:
        cuenta = get_object_or_404(CuentaPedido, id=cuenta_id, pedido=pedido)
    else:
        # Si no hay cuenta, intentamos obtener la primera o crear una global
        cuenta = pedido.cuentas.first()
        if not cuenta:
            # Lógica para crear la cuenta única si no se ha dividido
            cuenta = CuentaPedido.objects.create(pedido=pedido, nombre="Cuenta Única")
            # Asignar todos los detalles del pedido a esta cuenta
            pedido.detalles.update(cuenta=cuenta)
            cuenta.recalcular_totales()

    # 2. Usar los detalles de LA CUENTA, no de todo el pedido
    detalles_a_facturar = cuenta.detalles.all()
    
    items = []
    for detalle in detalles_a_facturar:
        items.append({
            "id": detalle.platillo.producto_id,
            "codigo": getattr(detalle.platillo, 'codigo', 'SERV'),
            "nombre": detalle.platillo.nombre,
            "precio": float(detalle.precio_unitario),
            "cantidad": int(detalle.cantidad),
            "desc_pct": float(detalle.descuento_pct),
            "iva_on": detalle.aplica_iva,
            "stock": 999 
        })

    # IMPORTANTE: Guardar el ID de la cuenta en la sesión para el receiver
    request.session["facturacion_prefill"] = {
        # "receptor_id": receptor.id,
        "items": items,
        "origen": "restaurante",
        "pedido_id": pedido.id,
        "cuenta_id": cuenta.id  # <-- Clave para cerrar la cuenta correcta
    }
    request.session.modified = True

    return redirect("/fe/generar/?from_cart=1&restaurante=1")

@login_required
@transaction.atomic
def cuenta_pagar(request, cuenta_id):
    # if getattr(request.user, "role", None) != "mesero":
    #     return HttpResponseForbidden("Solo meseros.")
    # mesero = get_mesero_from_user(request.user)

    cuenta = get_object_or_404(
        CuentaPedido.objects.select_for_update().select_related("pedido", "pedido__mesa"),
        id=cuenta_id,
        # pedido__mesero=mesero,
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
    # 1. Seguridad: solo meseros
    # if getattr(request.user, "role", None) not in ("mesero", "admin"):
    #     return HttpResponseForbidden("Solo meseros.")

    # mesero = get_mesero_from_user(request.user)
    # if not mesero:
    #     messages.error(request, "No tienes mesero asociado o estás inactivo.")
    #     return redirect("mesas-lista")

    # 2. Mesa
    mesa = get_object_or_404(Mesa, id=mesa_id)

    # 3. Pedido activo de esa mesa y mesero
    pedido = (
        Pedido.objects
        .select_for_update()
        .filter(
            mesa=mesa,
            # mesero=mesero,
            estado__in=["ABIERTO", "CERRADO"],
        )
        .order_by("-creado_el")
        .first()
    )
    if not pedido:
        messages.error(request, "No hay pedido pendiente en esta mesa.")
        return redirect("mesas-lista")

    # 4. Recalcular totales SOLO del pedido
    # (las cuentas, si existen, se recalculan en split / pago)
    pedido.recalcular_totales(save=True)

    # 5. Obtener cuentas (puede no haber ninguna)
    cuentas = pedido.cuentas.all().order_by("creado_el")

    # Consolidación de productos para la vista ---
    detalles_consolidados = {}
    for detalle in pedido.detalles.all():
        p_id = detalle.platillo.id
        if p_id not in detalles_consolidados:
            detalles_consolidados[p_id] = {
                'id': p_id,
                'nombre': detalle.platillo.nombre,
                'cantidad': detalle.cantidad,
                'total_linea': detalle.total_linea,
                'notas': [detalle.notas] if detalle.notas else []
            }
        else:
            detalles_consolidados[p_id]['cantidad'] += detalle.cantidad
            detalles_consolidados[p_id]['total_linea'] += detalle.total_linea
            if detalle.notas and detalle.notas not in detalles_consolidados[p_id]['notas']:
                detalles_consolidados[p_id]['notas'].append(detalle.notas)

    # 6. Renderizar vista de decisión
    return render(request, "pedidos/checkout.html", {
        "mesa": mesa,
        "pedido": pedido,
        "cuentas": cuentas,  # puede estar vacío y está bien
        "productos_consolidados": detalles_consolidados.values()
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
    if getattr(request.user, "role", None) != "mesero":
        return JsonResponse({"ok": False, "error": "Solo meseros."}, status=403)

    mesero = get_mesero_from_user(request.user)

    try:
        detalle_id = int(request.POST["detalle_id"])
        cuenta_destino_id = request.POST.get("cuenta_destino_id")  # "POOL" o id
        qty = int(request.POST.get("qty") or 1)
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)

    if qty == 0:
        return JsonResponse({"ok": False, "error": "qty no puede ser 0."}, status=400)
    qty = abs(qty)

    detalle_hint = get_object_or_404(DetallePedido, id=detalle_id, pedido__mesero=mesero)

    # destino
    if cuenta_destino_id in (None, "POOL", ""):
        cuenta_destino = None
    else:
        cuenta_destino = get_object_or_404(CuentaPedido, id=int(cuenta_destino_id), pedido=detalle_hint.pedido)

    pedido = detalle_hint.pedido
    platillo = detalle_hint.platillo

    # defaults de precio/iva/notas (tomados del detalle “hint”)
    src_defaults = {
        "precio_unitario": detalle_hint.precio_unitario,
        "descuento_pct": detalle_hint.descuento_pct,
        "aplica_iva": detalle_hint.aplica_iva,
        "notas": detalle_hint.notas,
    }

    # >>> Fuente REAL = la cuenta del detalle_hint (no solo esa fila), para evitar duplicados
    cuenta_origen = detalle_hint.cuenta  # None => POOL, o una cuenta
    qs_origen = DetallePedido.objects.filter(pedido=pedido, platillo=platillo, cuenta=cuenta_origen)

    total_origen = qs_origen.aggregate(s=Sum("cantidad"))["s"] or 0
    if qty > total_origen:
        return JsonResponse({"ok": False, "error": "Cantidad mayor a la disponible en el origen."}, status=400)

    # consumir del origen (sin borrar por PROTECT)
    _consume_qty(qs_origen, qty)

    # sumar al destino (consolidado)
    dest, created = _get_or_create_dest(pedido, platillo, cuenta_destino, src_defaults, qty=qty)
    if not created:
        dest.cantidad += qty
        dest.save(update_fields=["cantidad"])

    # recalcular
    pedido.recalcular_totales(save=True)
    if cuenta_destino:
        cuenta_destino.recalcular_totales(save=True)

    # mapa agregado (SUMADO)
    item_map = _build_item_map(pedido, platillo)

    # asegurar la llave del destino exista aunque quede 0
    if cuenta_destino is not None:
        item_map.setdefault(str(cuenta_destino.id), {"qty": 0, "detalle_id": None})

    return JsonResponse({"ok": True, "map": item_map})

@login_required
@require_POST
@transaction.atomic
def confirmar_division(request, pedido_id):
    # 1. Seguridad
    if getattr(request.user, "role", None) != "mesero":
        return HttpResponseForbidden("Solo meseros.")

    mesero = get_mesero_from_user(request.user)

    # 2. Pedido con lock
    pedido = get_object_or_404(
        Pedido.objects.select_for_update(),
        id=pedido_id,
        mesero=mesero,
        estado="CERRADO",
    )

    # 3. Debe haber cuentas
    cuentas = list(pedido.cuentas.select_for_update())

    if not cuentas:
        messages.error(request, "No hay cuentas creadas para dividir.")
        return redirect("pedido-split", pedido_id=pedido.id)

    # 4. Validación: NO productos sin asignar
    if pedido.detalles.filter(cuenta__isnull=True).exists():
        messages.error(
            request,
            "Hay productos sin asignar. Asigna todos antes de confirmar."
        )
        return redirect("pedido-split", pedido_id=pedido.id)

    # 5. Validación: NO cuentas vacías
    cuentas_vacias = [
        c.nombre for c in cuentas if not c.detalles.exists()
    ]
    if cuentas_vacias:
        messages.error(
            request,
            f"Las siguientes cuentas están vacías: {', '.join(cuentas_vacias)}"
        )
        return redirect("pedido-split", pedido_id=pedido.id)

    # 6. Validación: estados válidos
    if any(c.estado not in ("ABIERTA",) for c in cuentas):
        messages.error(
            request,
            "Hay cuentas que no están ABIERTAS y no pueden confirmarse."
        )
        return redirect("pedido-split", pedido_id=pedido.id)

    # 7. Recalcular totales por cuenta
    for c in cuentas:
        c.recalcular_totales(save=True)

    # 8. Cerrar cuentas
    pedido.cuentas.filter(estado="ABIERTA").update(
        estado="CERRADA",
        cerrado_el=timezone.now()
    )

    # 9. Marcar pedido como split confirmado
    pedido.division_confirmada = True
    pedido.save(update_fields=["division_confirmada"])

    messages.success(
        request,
        "División confirmada. Ya puedes cobrar o facturar por cuenta."
    )

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

@login_required
@transaction.atomic
def entregar_pedido(request, mesa_id):
    if not Caja.objects.filter(estado="ABIERTA").exists():
        messages.error(request, "Denegado: No hay una caja abierta.", extra_tags="error-caja-cerrada")
        return redirect("mesas-lista")
    
    mesa = get_object_or_404(Mesa, id=mesa_id)
    pedido = Pedido.objects.filter(mesa=mesa, estado='ABIERTO').first()
    
    if pedido:
        comanda = Comanda.objects.filter(pedido_id=pedido.id).first()
        
        # Corrección: Acceder al atributo .estado
        if comanda and comanda.estado == "CERRADA":
            mesa.estado = 'ENTREGADO'
            mesa.save()
            messages.success(request, f"¡Éxito! Pedido de mesa {mesa.numero} entregado.")
        else:
            messages.warning(request, "La comida aún no ha sido marcada como lista en cocina.")
    
    return redirect("mesas-lista")