from datetime import timezone
from decimal import Decimal
import logging
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import transaction
from FE.models import Emisor_fe, Receptor_fe
from FE.utils import _get_emisor_for_user
from RESTAURANTE.models import Caja, CategoriaMenu, Comanda, CuentaPedido, DetallePedido, Mesa, Mesero, Pedido, Platillo
from RESTAURANTE.services.services_comandas import enviar_pedido_a_cocina
from RESTAURANTE.services.services_pedidos import crear_map_json_por_item
from django.db.models import Sum, F

from RESTAURANTE.views.views_cuentas import _build_item_map, _consume_qty, _get_or_create_dest

from django.core.paginator import Paginator
import json

logger = logging.getLogger(__name__)


def _calcular_propina(base: Decimal, mesa, emisor) -> Decimal:
    """
    Devuelve el monto de propina sugerida para `base`.
    Prioridad: mesa.propina_porcentaje → emisor.config_tip.porcentaje → 0
    """
    porcentaje = None
    if mesa and mesa.propina_porcentaje is not None:
        porcentaje = mesa.propina_porcentaje
    elif emisor and getattr(emisor, "es_restaurante", False):
        config = getattr(emisor, "config_tip", None)
        if config:
            porcentaje = config.porcentaje
    if porcentaje is None:
        return Decimal("0.00")
    return (base * porcentaje / Decimal("100")).quantize(Decimal("0.01"))


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
def guardar_detalles_desde_json(pedido, platillos_json: str, *, modo="append"):
    try:
        items = json.loads(platillos_json or "[]")
    except json.JSONDecodeError:
        items = []

    # 1. Agrupar items del JSON
    qty_map = {}
    for it in items:
        pid = str(it.get("id") or "")
        if not pid: continue
        qty = int(it.get("qty") or 1)
        qty_map[pid] = qty_map.get(pid, 0) + qty

    if not qty_map: return

    if modo == "set":
        pedido.detalles.all().delete()

    # 2. Procesar Platillos
    platillos = Platillo.objects.filter(id__in=list(qty_map.keys()), disponible=True)
    
    for p in platillos:
        cantidad_nueva = qty_map[str(p.id)]

        detalle, created = DetallePedido.objects.get_or_create(
            pedido=pedido,
            platillo=p,
            defaults={
                'cantidad': cantidad_nueva,
                'precio_unitario': p.precio_venta,
                'aplica_iva': True,
            }
        )

        if not created:
            # ✅ SOLUCIÓN AL ERROR DECIMAL: 
            # En lugar de F() directo en el objeto antes del save(),
            # usamos update() para que el cálculo ocurra solo en SQL
            DetallePedido.objects.filter(id=detalle.id).update(
                cantidad=F('cantidad') + cantidad_nueva
            )
            # Ahora refrescamos el objeto para que self.cantidad sea un número real
            detalle.refresh_from_db()
            # Llamamos a save() (que disparará _calc) ya con valores numéricos
            detalle.save() 
        else:
            # Si es nuevo, el default ya es un entero, _calc() funcionará bien en el save()
            pass 

    # 3. Finalizar totales
    pedido.refresh_from_db()
    pedido.recalcular_totales(save=True)
    
@login_required
@transaction.atomic
def tomar_pedido(request, mesa_id):
    logger.debug("REQUEST %s", request.method)
    """
    Crea/reutiliza un Pedido ABIERTO para la mesa.
    - Si mesa está PENDIENTE_ORDEN o OCUPADA: ok
    - Si LIBRE: opcionalmente puedes pasarla a PENDIENTE_ORDEN aquí
    """

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
    q = (request.GET.get("q") or "").strip()
    f_cat = (request.GET.get("cat") or "").strip()

    queryset = (
        Platillo.objects
        .filter(disponible=True)
        .select_related("categoria")
        .order_by("categoria__nombre", "nombre")
    )

    if q:
        queryset = queryset.filter(nombre__icontains=q)

    if f_cat:
        try:
            queryset = queryset.filter(categoria_id=int(f_cat))
        except ValueError:
            pass

    paginator = Paginator(queryset, 12)  # pon el tamaño que quieras
    page_number = request.GET.get("page")
    platillos_paginados = paginator.get_page(page_number)
    detalles = pedido.detalles.select_related("platillo").all().order_by("id")
    categorias = CategoriaMenu.objects.all().order_by("nombre")
    
    context = {
        "mesa": mesa,
        "pedido": pedido,
        "platillos": platillos_paginados,
        "detalles": detalles,
        "q": q,
        "f_cat": f_cat,
        "categorias": categorias,   # ✅ para los tags
    }
    
    if request.headers.get("HX-Request"):
        return render(request, "pedidos/menu_seleccion_pedido.html", context)

    return render(request, "pedidos/_toma_pedido.html", context)



@login_required
@transaction.atomic
def solicitar_cuenta(request, mesa_id):
    """
    Cambia el estado de la mesa a Pendiente de pago e imprime el ticket de prefactura
    """
    
    if not Caja.objects.filter(estado="ABIERTA").exists():
        messages.error(request, "Denegado: No hay una caja abierta.", extra_tags="error-caja-cerrada")
        return redirect("mesas-lista")
    
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    # Buscamos el pedido abierto más reciente de esta mesa
    pedido = Pedido.objects.filter(mesa=mesa, estado="ABIERTO").first()

    if not pedido:
        messages.warning(request, f"No se encontró un pedido abierto para la Mesa {mesa.numero}.")
        return redirect("mesas-lista")

    mesa.estado="PENDIENTE_PAGO"
    mesa.save()
    
    emisor = _get_emisor_for_user(request.user, estricto=False)

    propina_monto = _calcular_propina(pedido.total, mesa, emisor)
    total_con_propina = pedido.total + propina_monto

    detalles = DetallePedido.objects.filter(pedido=pedido)

    logger.debug("DETALLES ******* %s", detalles)
    
    return render(request, "documentos/template_ticket_cuenta_total.html", {
        "pedido": pedido,
        "detalle_items": detalles,
        "emisor": emisor,
        "propina_monto": propina_monto,
        "total_con_propina": total_con_propina
    })
    # print(">>>MESA ", mesa)
    # print(">>>MESA ", mesa)
    
    # messages.success(request, f'Mesa {mesa.numero} ahora está OCUPADA.')
    
    # messages.success(request, "Pedido enviado a cobro (pendiente de pago).")
    # return redirect("mesas-lista")

@login_required
@transaction.atomic
def pedido_crear_desde_mesa(request):
    if not Caja.objects.filter(estado="ABIERTA").exists():
        messages.error(request, "Denegado: No hay una caja abierta.", extra_tags="error-caja-cerrada")
        return redirect("mesas-lista")
    
    logger.debug("request.method %s", request.method)

    if request.method == "POST":
        mesero = get_mesero_from_user(request.user) # obtener el mesero que esta loggeado
        if not mesero:
            logger.warning("No tienes un mesero asociado o estás inactivo.")
            return redirect("mesas-lista")

        logger.debug("mesero %s", mesero)
        

        mesa_id = request.POST.get("mesa_id") 
        notas = (request.POST.get("notas") or "").strip()
        receptor_id = request.POST.get("receptor_id") or None

        mesa = get_object_or_404(Mesa.objects.select_for_update(), id=mesa_id)
        logger.debug("mesa %s", mesa)
        logger.debug("mesa.estado %s", mesa.estado)

        if mesa.estado not in ("PENDIENTE_ORDEN", "OCUPADA", "ENTREGADO"):
            messages.error(request, f"Estado de mesa no válido: {mesa.estado}")
            return redirect("mesas-lista")

        pedido, created = Pedido.objects.select_for_update().get_or_create(
            mesa=mesa, 
            estado="ABIERTO", 
            mesero=mesero,
            defaults={'estado': 'ABIERTO'}
        )
        
        logger.debug("pedido %s", pedido)

        if receptor_id:
            pedido.receptor = get_object_or_404(Receptor_fe, id=receptor_id)
        if notas:
            pedido.notas = notas
        pedido.save()

        logger.debug("POST keys: %s", list(request.POST.keys()))
        logger.debug("platillos_json: %s", request.POST.get("platillos_json"))

        # ✅ GUARDAR DETALLES
        # En pedido_crear_desde_mesa
        platillos_json = request.POST.get("platillos_json", "[]")

        # IMPORTANTE: 
        # Si el pedido ya existía, queremos SUMAR (append), no REEMPLAZAR (set).
        if created:
            guardar_detalles_desde_json(pedido, platillos_json, modo="set")
        else:
            # Esta lógica debes implementarla en tu helper para que busque si el plato 
            # ya existe en el pedido y sume la cantidad, o cree una línea nueva.
            guardar_detalles_desde_json(pedido, platillos_json, modo="append")
            
        tiene_detalles = pedido.detalles.all().exists()
        logger.debug("TIENE DETALLES %s", pedido.detalles)
        logger.debug("TIENE DETALLES %s", tiene_detalles)
        if tiene_detalles:
            # ✅ Cambiar estado de la mesa a OCUPADA
            if mesa.estado != "OCUPADA":
                mesa.estado = "OCUPADA"
                mesa.save() # Quitamos update_fields para asegurar el guardado total o verificar signals

            logger.info("Pedido %s", pedido)
            logger.info("Pedido id %s", pedido.id)
            logger.info("tiene_detalles %s", tiene_detalles)

            # ✅ ENVIAR A COCINA
            comanda = enviar_pedido_a_cocina(pedido, notas=notas)
            logger.info("comanda %s", comanda)
            
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

# @csrf_exempt
@require_POST
@transaction.atomic
def split_detalle_pedido(request):
    data = json.loads(request.body)

    detalle_id = data.get("detalle_id")
    split_data = data.get("split", {})

    if not detalle_id or not split_data:
        return JsonResponse(
            {"error": "Datos incompletos"},
            status=400
        )

    detalle = get_object_or_404(
        DetallePedido.objects.select_for_update(),
        id=detalle_id
    )

    # convertir a int
    distribucion = {
        int(k): int(v)
        for k, v in split_data.items()
        if int(v) > 0
    }

    if sum(distribucion.values()) != detalle.cantidad:
        return JsonResponse(
            {"error": "La suma del split no coincide con la cantidad"},
            status=400
        )

    nuevos = detalle.split(distribucion)

    pedido = detalle.pedido
    pedido.recalcular_totales(save=True)

    return JsonResponse({
        "ok": True,
        "pedido_id": pedido.id,
        "cuentas": [
            {
                "id": c.id,
                "total": float(c.total),
                "detalles": [
                    {
                        "id": d.id,
                        "platillo": d.platillo.nombre,
                        "platillo_id": d.platillo_id,
                        "cantidad": d.cantidad,
                        "precio": float(d.precio_unitario),
                    }
                    for d in c.detalles.all()
                ]
            }
            for c in pedido.cuentas.all()
        ],
        "pool": list(
            pedido.detalles
            .filter(cuenta__isnull=True)
            .values("platillo_id", "cantidad")
        )
    })

    
@login_required
@transaction.atomic
def pedido_split(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects.select_for_update(),
        id=pedido_id
    )

    cuentas = pedido.cuentas.all()

    # 🔥 AUTO-POOL: si solo hay una cuenta y no hay pool
    if cuentas.count() == 1 and not pedido.detalles.filter(cuenta__isnull=True).exists():
        unica = cuentas.first()
        pedido.detalles.filter(cuenta=unica).update(cuenta=None)

    cuentas = pedido.cuentas.prefetch_related("detalles__platillo")

    pool_detalles = (
        pedido.detalles
        .filter(cuenta__isnull=True)
        .values(
            "platillo_id",
            "platillo__nombre",
            "precio_unitario",
        )
        .annotate(cantidad=Sum("cantidad"))
        .filter(cantidad__gt=0)
    )

    context = {
        "pedido": pedido,
        "cuentas": cuentas,
        "pool_detalles": pool_detalles,
    }

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

    if pedido.estado not in ("ABIERTO", "CERRADO"):
        messages.error(request, "Esta cuenta no está disponible para cobro.")
        return redirect("pedido-checkout", pedido.mesa_id)

    if cuenta.estado not in ("ABIERTA", "CERRADA"):
        messages.error(request, "Esta cuenta ya fue pagada o anulada.")
        return redirect("pedido-checkout", pedido.mesa_id)

    if request.method == "POST":
        forma_pago = request.POST.get("forma_pago", "01")  # "01"=efectivo, "03"=tarjeta

        # Cerrar pedido si aún está abierto
        if pedido.estado == "ABIERTO":
            pedido.cerrar()

        cuenta.estado = "PAGADA"
        from django.utils import timezone as dj_tz
        cuenta.pagado_el = dj_tz.now()
        cuenta.save(update_fields=["estado", "pagado_el"])

        # Registrar en Caja
        caja_actual = Caja.objects.filter(estado="ABIERTA").first()
        if caja_actual:
            monto = Decimal(str(cuenta.total or 0))
            caja_actual.total_ventas  = Decimal(str(caja_actual.total_ventas  or 0)) + monto
            if forma_pago == "03":
                caja_actual.total_tarjeta  = Decimal(str(caja_actual.total_tarjeta  or 0)) + monto
            else:
                caja_actual.total_efectivo = Decimal(str(caja_actual.total_efectivo or 0)) + monto
            caja_actual.save(update_fields=["total_ventas", "total_efectivo", "total_tarjeta"])

        pedido.marcar_pagado_si_corresponde()

        return redirect("imprimir-ticket-cuenta", cuenta_id=cuenta.id)

    return render(request, "pedidos/checkout.html", {
        "mesa": pedido.mesa,
        "pedido": pedido,
        "cuentas": pedido.cuentas.all(),
        "productos_consolidados": _consolidar_productos(pedido),
        "cuenta_activa": cuenta,
    })

# Seleccionar pago en una sola cuenta o cuentas separadas y añadir cuenta predeterminada (una sola cuenta)
@login_required
@transaction.atomic
def pedido_checkout(request, mesa_id):
    # 1. Seguridad: solo meseros
    if getattr(request.user, "role", None) not in ("cajero", "admin"):
        return HttpResponseForbidden("Solo meseros.")

    # mesero = get_mesero_from_user(request.user)
    # if not mesero:
    #     messages.error(request, "No tienes mesero asociado o estás inactivo.")
    #     return redirect("mesas-lista")

    # 2. Mesa
    if not Caja.objects.filter(estado="ABIERTA").exists():
        messages.error(request, "Denegado: No hay una caja abierta.", extra_tags="error-caja-cerrada")
        return redirect("mesas-lista")
    
    mesa = get_object_or_404(Mesa, id=mesa_id)
    
    # 3. Pedido activo de esa mesa y mesero
    pedido = (
        Pedido.objects
        .select_for_update()
        .filter(
            mesa=mesa,
            estado__in=["ABIERTO"],
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

    # 6. Renderizar vista de decisión
    return render(request, "pedidos/checkout.html", {
        "mesa": mesa,
        "pedido": pedido,
        "cuentas": cuentas,
        "productos_consolidados": list(_consolidar_productos(pedido)),
    })

def _consolidar_productos(pedido):
    """Helper: consolida detalles del pedido por platillo."""
    result = {}
    for detalle in pedido.detalles.all():
        p_id = detalle.platillo_id
        if p_id not in result:
            result[p_id] = {
                "id": p_id,
                "nombre": detalle.platillo.nombre,
                "cantidad": detalle.cantidad,
                "total_linea": detalle.total_linea,
                "notas": [detalle.notas] if detalle.notas else [],
            }
        else:
            result[p_id]["cantidad"] += detalle.cantidad
            result[p_id]["total_linea"] += detalle.total_linea
            if detalle.notas and detalle.notas not in result[p_id]["notas"]:
                result[p_id]["notas"].append(detalle.notas)
    return result.values()


@login_required
@require_POST
@transaction.atomic
def cobrar_total(request, mesa_id):
    """Cobra el pedido completo en una sola cuenta (sin facturación electrónica)."""
    from django.utils import timezone as dj_tz

    mesa = get_object_or_404(Mesa, id=mesa_id)
    pedido = (
        Pedido.objects.select_for_update()
        .filter(mesa=mesa, estado__in=["ABIERTO", "CERRADO"])
        .order_by("-creado_el")
        .first()
    )
    if not pedido:
        messages.error(request, "No hay pedido activo en esta mesa.")
        return redirect("mesas-lista")

    forma_pago = request.POST.get("forma_pago", "01")  # "01"=efectivo, "03"=tarjeta

    # Obtener o crear cuenta única
    cuenta = pedido.cuentas.filter(estado__in=["ABIERTA", "CERRADA"]).first()
    if not cuenta:
        cuenta = CuentaPedido.objects.create(pedido=pedido, nombre="Cuenta")

    # Asignar todos los detalles sin cuenta a esta
    pedido.detalles.filter(cuenta__isnull=True).update(cuenta=cuenta)
    cuenta.recalcular_totales(save=True)
    pedido.recalcular_totales(save=True)

    # Cerrar pedido si aún está abierto
    if pedido.estado == "ABIERTO":
        pedido.cerrar()

    # Marcar cuenta como pagada
    cuenta.estado = "PAGADA"
    cuenta.pagado_el = dj_tz.now()
    cuenta.save(update_fields=["estado", "pagado_el"])

    # Registrar en caja
    caja_actual = Caja.objects.filter(estado="ABIERTA").first()
    if caja_actual:
        monto = Decimal(str(cuenta.total or 0))
        caja_actual.total_ventas  = Decimal(str(caja_actual.total_ventas  or 0)) + monto
        if forma_pago == "03":
            caja_actual.total_tarjeta  = Decimal(str(caja_actual.total_tarjeta  or 0)) + monto
        else:
            caja_actual.total_efectivo = Decimal(str(caja_actual.total_efectivo or 0)) + monto
        caja_actual.save(update_fields=["total_ventas", "total_efectivo", "total_tarjeta"])

    pedido.marcar_pagado_si_corresponde()

    return redirect("imprimir-ticket-cuenta", cuenta_id=cuenta.id)


@login_required
def imprimir_pre_ticket(request, mesa_id):
    """Imprime pre-cuenta sin cambiar el estado del pedido."""
    mesa = get_object_or_404(Mesa, id=mesa_id)
    pedido = (
        Pedido.objects.filter(mesa=mesa, estado__in=["ABIERTO", "CERRADO"])
        .order_by("-creado_el")
        .first()
    )
    if not pedido:
        return redirect("mesas-lista")

    emisor = _get_emisor_for_user(request.user, estricto=False)
    propina_monto = _calcular_propina(pedido.total, mesa, emisor)
    total_con_propina = pedido.total + propina_monto

    return render(request, "documentos/template_ticket_cuenta_total.html", {
        "pedido": pedido,
        "detalle_items": pedido.detalles.select_related("platillo").all(),
        "emisor": emisor,
        "propina_monto": propina_monto,
        "total_con_propina": total_con_propina,
    })


@login_required
def imprimir_ticket_cuenta(request, cuenta_id):
    """Imprime ticket de una cuenta específica (post-pago)."""
    cuenta = get_object_or_404(
        CuentaPedido.objects.select_related("pedido__mesa"),
        id=cuenta_id,
    )
    pedido = cuenta.pedido
    mesa = pedido.mesa
    emisor = _get_emisor_for_user(request.user, estricto=False)
    propina_monto = _calcular_propina(cuenta.total, mesa, emisor)
    total_con_propina = cuenta.total + propina_monto

    return render(request, "documentos/ticket_cuenta_pagada.html", {
        "pedido": pedido,
        "cuenta": cuenta,
        "detalle_items": cuenta.detalles.select_related("platillo").all(),
        "emisor": emisor,
        "propina_monto": propina_monto,
        "total_con_propina": total_con_propina,
    })


# Agregar mas cuentas en la division de cuentas
@login_required
@require_POST
@transaction.atomic
def crear_cuenta_extra(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects.select_for_update(),
        id=pedido_id
    )

    num_cuentas = pedido.cuentas.count() + 1

    CuentaPedido.objects.create(
        pedido=pedido,
        nombre=f"Cuenta {num_cuentas}",
        estado="ABIERTA"
    )

    return JsonResponse({"ok": True})





@require_POST
@transaction.atomic
def mover_detalle(request):
    data = json.loads(request.body)
    delta = int(data.get("delta", 0))

    # ➕ TOMAR DEL POOL
    if delta > 0:
        platillo_id = data.get("platillo_id")
        cuenta_id = data.get("cuenta_id")

        if not platillo_id or not cuenta_id:
            return JsonResponse(
                {"ok": False, "error": "Faltan datos (platillo o cuenta)"},
                status=400
            )

        try:
            platillo_id = int(platillo_id)
            cuenta_id = int(cuenta_id)
        except ValueError:
            return JsonResponse(
                {"ok": False, "error": "IDs inválidos"},
                status=400
            )

        pool = (
            DetallePedido.objects
            .select_for_update()
            .filter(
                pedido__cuentas__id=cuenta_id,
                platillo_id=platillo_id,
                cuenta__isnull=True,
                cantidad__gt=0
            )
            .order_by("-cantidad")
            .first()
        )

        if not pool:
            return JsonResponse(
                {"ok": False, "error": "No disponible"},
                status=400
            )

        # restar del pool
        pool.cantidad -= 1
        pool.save()

        # sumar en cuenta
        detalle_cuenta, _ = DetallePedido.objects.get_or_create(
            pedido=pool.pedido,
            platillo=pool.platillo,
            cuenta_id=cuenta_id,
            defaults={
                "cantidad": 0,
                "precio_unitario": pool.precio_unitario,
                "descuento_pct": pool.descuento_pct,
                "aplica_iva": pool.aplica_iva,
                "notas": pool.notas,
            }
        )
        detalle_cuenta.cantidad += 1
        detalle_cuenta.save()

        pedido = pool.pedido

    # ➖ DEVOLVER AL POOL
    else:
        detalle_id = data.get("detalle_id")

        if not detalle_id:
            return JsonResponse(
                {"ok": False, "error": "Falta detalle"},
                status=400
            )

        detalle = get_object_or_404(
            DetallePedido.objects.select_for_update(),
            id=detalle_id
        )

        pedido = detalle.pedido

        detalle.cantidad -= 1
        detalle.save()

        pool, _ = DetallePedido.objects.get_or_create(
            pedido=pedido,
            platillo=detalle.platillo,
            cuenta__isnull=True,
            defaults={
                "cantidad": 0,
                "precio_unitario": detalle.precio_unitario,
                "descuento_pct": detalle.descuento_pct,
                "aplica_iva": detalle.aplica_iva,
                "notas": detalle.notas,
            }
        )
        pool.cantidad += 1
        pool.save()

    pedido.recalcular_totales(save=True)

    cuenta = None
    if delta > 0:
        cuenta = detalle_cuenta.cuenta
    else:
        cuenta = detalle.cuenta

    return JsonResponse({
        "ok": True,
        "cuenta": {
            "id": cuenta.id,
            "total": float(cuenta.total),
            "detalles": [
                {
                    "id": d.id,
                    "platillo_id": d.platillo_id,
                    "platillo__nombre": d.platillo.nombre,
                    "cantidad": d.cantidad,
                    "precio_unitario": float(d.precio_unitario),
                }
                for d in cuenta.detalles.select_related("platillo")
            ]
        },
        "pool": [
            {
                "platillo_id": p["platillo_id"],
                "cantidad": p["cantidad"],
            }
            for p in (
                pedido.detalles
                .filter(cuenta__isnull=True)
                .values("platillo_id")
                .annotate(cantidad=Sum("cantidad"))
                .filter(cantidad__gt=0)
            )
        ]
    })



@login_required
@require_POST
@transaction.atomic
def confirmar_division(request, pedido_id):
    # 1. Seguridad
    # if getattr(request.user, "role", None) != "mesero":
    #     return HttpResponseForbidden("Solo meseros.")

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
    # if getattr(request.user, "role", None) != "mesero":
    #     return HttpResponseForbidden("Solo meseros.")    
    logger.info("CUENTA_ID %s", cuenta_id)
    
    cuenta = get_object_or_404(
        CuentaPedido.objects.select_for_update().select_related("pedido"),
        id=cuenta_id,
    )
    
    logger.debug("CUENTA %s", cuenta)

    pedido = cuenta.pedido

    logger.debug("pedido %s", pedido)

    # if pedido.estado != "CERRADO":
    #     messages.error(request, "El pedido debe estar CERRADO para facturar.")

    #     return redirect("mesas-lista")
    logger.debug("pedido 2 %s", pedido)

    # si es split confirmado, exigimos CERRADA
    if pedido.division_confirmada and cuenta.estado != "CERRADA":
        messages.error(request, "La cuenta debe estar CERRADA (confirmada) para facturar.")
        logger.debug("pedido.division_confirmada 2 %s", pedido.division_confirmada)
        
        return redirect("pedido-checkout", mesa_id=pedido.mesa_id)

    logger.debug("pedido.division_confirmada %s", pedido.division_confirmada)


    receptor = Receptor_fe.objects.filter(num_documento="00000000-0").first()
    if not receptor:
        messages.error(request, "No se encontró receptor por defecto (00000000-0).")
        return redirect("pedido-checkout", mesa_id=pedido.mesa_id)
    logger.debug("cuenta.estado %s", cuenta.estado)

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
    logger.info("REDIRIGIENDO A FACTURACION... ")
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


@login_required
@transaction.atomic
def cambio_nombre_cuenta(request, cuenta_id):
    logger.debug("PRINRRRRRRRR %s", request.method)
    nuevo_nombre = request.POST.get("name") 
    cuenta = get_object_or_404(
        CuentaPedido.objects.select_for_update().select_related("pedido"),
        id=cuenta_id,
    )
    
    cuenta.nombre = nuevo_nombre
    cuenta.save()    
    
    return redirect("pedido-split", cuenta.pedido.id)

@login_required
@transaction.atomic
def eliminar_cuenta_extra(request, cuenta_id):
    cuenta = get_object_or_404(
        CuentaPedido.objects.select_for_update().select_related("pedido"),
        id=cuenta_id,
    )
    pedido = cuenta.pedido

    # 🔁 devolver detalles al pool
    for d in cuenta.detalles.select_for_update():
        pool, _ = DetallePedido.objects.get_or_create(
            pedido=pedido,
            platillo=d.platillo,
            cuenta__isnull=True,
            defaults={
                "cantidad": 0,
                "precio_unitario": d.precio_unitario,
                "descuento_pct": d.descuento_pct,
                "aplica_iva": d.aplica_iva,
                "notas": d.notas,
            }
        )
        pool.cantidad += d.cantidad
        pool.save()

    # eliminar los detalles de la cuenta
    cuenta.detalles.all().delete()

    # ahora sí eliminar la cuenta
    cuenta.delete()

    pedido.recalcular_totales(save=True)

    return redirect("pedido-split", pedido.id)
