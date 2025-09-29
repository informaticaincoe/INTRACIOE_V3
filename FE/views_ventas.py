# =========================
#   VENTAS (front-office)
# =========================
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from django.db.models import Q, F, Sum, Count
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
import requests
from django.utils import timezone
from django.views.decorators.http import require_http_methods
#from django.contrib.auth.models import User  # si usas auth default
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from django.db.models import FloatField, F, ExpressionWrapper
from math import radians, cos, sin, asin, sqrt

# Modelos FE
from .models import NumeroControl, Receptor_fe, TiposDocIDReceptor, Municipio, Tipo_dte, Modelofacturacion, TipoTransmision
from .models import FacturaElectronica, DetalleFactura, Descuento
# Modelos INVENTARIO
from INVENTARIO.models import Producto, MovimientoInventario, DevolucionVenta, DetalleDevolucionVenta, Almacen, Tributo, TipoItem, TipoUnidadMedida

CART_SESSION_KEY = "cart_by_receptor"    # { "<receptor_id>": { "<producto_id>": {qty, precio, iva_on, desc_pct} } }


from django.contrib.auth import get_user_model

User = get_user_model()

def _get_cart(request):
    cart = request.session.get(CART_SESSION_KEY) or {}
    if not isinstance(cart, dict):
        cart = {}
    return cart

def _save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True

def _ensure_receptor(receptor_id):
    if not receptor_id:
        return None
    try:
        return Receptor_fe.objects.get(id=receptor_id)
    except Receptor_fe.DoesNotExist:
        return None
# ------------- EXPORTACIONES -------------

@login_required
def exportar_facturas_excel(request):
    # aplicar mismos filtros que en tu lista
    qs = FacturaElectronica.objects.select_related("dtereceptor", "tipo_dte").all()

    if request.GET.get("recibido_mh"):
        qs = qs.filter(recibido_mh=(request.GET["recibido_mh"] == "True"))
    if request.GET.get("tipo_dte"):
        qs = qs.filter(tipo_dte_id=request.GET["tipo_dte"])
    if request.GET.get("sello_recepcion"):
        qs = qs.filter(sello_recepcion__icontains=request.GET["sello_recepcion"])

    # Crear workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Facturas"

    # Encabezados
    headers = ["Número de Control", "Cliente", "Tipo DTE", "Fecha", "Total", "IVA", "Recibido MH", "Estado"]
    ws.append(headers)

    for factura in qs:
        ws.append([
            factura.numero_control,
            factura.dtereceptor.nombre if factura.dtereceptor else "",
            factura.tipo_dte.descripcion if factura.tipo_dte else "",
            factura.fecha_emision.strftime("%Y-%m-%d") if factura.fecha_emision else "",
            float(factura.total_pagar or 0),
            float(factura.total_iva or 0),
            "Sí" if factura.recibido_mh else "No",
            "Anulada" if factura.dte_invalidacion.exists() else "Viva"
        ])

    # Ajustar ancho de columnas
    for col_num, _ in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(col_num)].width = 20

    # Preparar respuesta
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="facturas.xlsx"'
    wb.save(response)
    return response



@login_required
def exportar_facturas_pdf(request):
    qs = FacturaElectronica.objects.select_related("dtereceptor", "tipo_dte").prefetch_related("detalles__producto")

    # aplicar filtros
    if request.GET.get("recibido_mh"):
        qs = qs.filter(recibido_mh=(request.GET["recibido_mh"] == "True"))
    if request.GET.get("tipo_dte"):
        qs = qs.filter(tipo_dte_id=request.GET["tipo_dte"])

    # totales de facturas
    total_facturas = qs.count()
    total_monto = qs.aggregate(Sum("total_pagar"))["total_pagar__sum"] or 0
    total_iva = qs.aggregate(Sum("total_iva"))["total_iva__sum"] or 0

    # totales de productos
    from .models import DetalleFactura
    detalles = DetalleFactura.objects.filter(factura__in=qs)

    total_lineas = detalles.count()
    total_cantidad = detalles.aggregate(Sum("cantidad"))["cantidad__sum"] or 0

    html_string = render_to_string("reportes/facturas_pdf.html", {
        "facturas": qs,
        "total_facturas": total_facturas,
        "total_monto": total_monto,
        "total_iva": total_iva,
        "total_lineas": total_lineas,
        "total_cantidad": total_cantidad,
        "filtros": request.GET,
    })
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="facturas.pdf"'
    return response


# ---------- HOME VENTAS ----------
@login_required
def ventas_home(request):
    return render(request, 'ventas/home.html')

# --------- CLIENTES (Receptor_fe) ----------
def _parse_coord(val):
    try:
        if val in (None, "", "null"):
            return None
        # Normalizar: convertir comas decimales a puntos
        val = str(val).strip().replace(",", ".")
        # Convertir a Decimal manteniendo todos los decimales
        return Decimal(val)
    except (InvalidOperation, ValueError, TypeError):
        return None
     
@login_required
def _geocode_address_osm(q):
    """
    Geocodifica con Nominatim (OSM).
    Respeta su política: añade User-Agent propio.
    """
    try:
        r = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={'q': q, 'format': 'json', 'addressdetails': 0, 'limit': 1},
            headers={'User-Agent': 'INTRACIOE/1.0 (+https://intracioe.com)'},
            timeout=5,
            )
        r.raise_for_status()
        data = r.json()
        if data:
            return Decimal(data[0]['lat']), Decimal(data[0]['lon']), "nominatim"
    except Exception:
        pass
    return None, None, ""


def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en km entre dos puntos (lat/lng)
    """
    # Aseguramos que todo sea float
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

    R = 6378  # Radio de la Tierra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

@login_required
def clientes_list(request):
    q = request.GET.get('q', '')
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    clientes = Receptor_fe.objects.all().order_by('nombre')
    if q:
        clientes = clientes.filter(nombre__icontains=q) | clientes.filter(num_documento__icontains=q)

    lat_user, lng_user = None, None
    if lat and lng:
        try:
            lat_user = float(lat)
            lng_user = float(lng)
            # calcular distancia en Python para cada cliente
            for c in clientes:
                if c.lat and c.lng:
                    c.distancia_km = round(haversine(lat_user, lng_user, c.lat, c.lng), 2)
                else:
                    c.distancia_km = None
            # ordenar por distancia
            clientes = sorted(clientes, key=lambda x: x.distancia_km if x.distancia_km is not None else 999999)
        except ValueError:
            pass

    # Paginación
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    clientes_page = paginator.get_page(page_number)

    return render(request, 'ventas/clientes/list.html', {
        'clientes': clientes_page,
        'q': q,
        'lat': lat_user,
        'lng': lng_user,
    })


@login_required
@require_http_methods(["GET", "POST"])
def clientes_crear(request):
    tipos = TiposDocIDReceptor.objects.all().order_by('descripcion')
    municipios = Municipio.objects.select_related('departamento').order_by('descripcion')

    if request.method == 'POST':
        tipo_id = request.POST.get('tipo_documento')
        num_documento = request.POST.get('num_documento')
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        municipio_id = request.POST.get('municipio')
        nrc = request.POST.get('nrc') or None

        # coordenadas del form (pueden venir vacías)
        lat = _parse_coord(request.POST.get('lat'))
        lng = _parse_coord(request.POST.get('lng'))

        geocode_source = ""
        geocoded_at = None

        if not (tipo_id and num_documento and nombre and municipio_id):
            messages.error(request, 'Complete los campos obligatorios.')
            return redirect('clientes_crear')

        tipo = get_object_or_404(TiposDocIDReceptor, pk=tipo_id)
        municipio = get_object_or_404(Municipio, pk=municipio_id)


        if (lat is None or lng is None) and direccion:
            # auto-geocode
            muni = municipio.descripcion if hasattr(municipio, "descripcion") else ""
            depto = getattr(getattr(municipio, "departamento", None), "descripcion", "")
            query = f"{direccion}, {muni}, {depto}, El Salvador"
            lat, lng, geocode_source = _geocode_address_osm(query)
            if lat is not None and lng is not None:
                geocoded_at = timezone.now()
        elif lat is not None and lng is not None:
            # 👇 si viene del mapa o "usar mi ubicación"
            geocode_source = "manual"
            geocoded_at = timezone.now()

        Receptor_fe.objects.create(
            tipo_documento=tipo, num_documento=num_documento, nombre=nombre,
            direccion=direccion, telefono=telefono, correo=correo,
            municipio=municipio, nrc=nrc,
            lat=lat, lng=lng, geocode_source=geocode_source, geocoded_at=geocoded_at
        )

        messages.success(request, 'Cliente creado.')
        return redirect('clientes_list')

    return render(
        request,
        'ventas/clientes/form.html',
        {'tipos': tipos, 'municipios': municipios}
    )

@login_required
def clientes_editar(request, pk):
    c = get_object_or_404(Receptor_fe, pk=pk)
    tipos = TiposDocIDReceptor.objects.all().order_by('descripcion')
    municipios = Municipio.objects.select_related('departamento').order_by('descripcion')

    if request.method == 'POST':
        tipo_id = request.POST.get('tipo_documento')
        municipio_id = request.POST.get('municipio')
        c.tipo_documento = get_object_or_404(TiposDocIDReceptor, pk=tipo_id) if tipo_id else c.tipo_documento
        c.num_documento = request.POST.get('num_documento') or c.num_documento
        c.nombre = request.POST.get('nombre') or c.nombre
        c.direccion = request.POST.get('direccion') or ''
        c.telefono = request.POST.get('telefono') or ''
        c.correo = request.POST.get('correo') or ''
        c.nrc = request.POST.get('nrc') or None

        # ✅ guardar coords del formulario
        c.lat = _parse_coord(request.POST.get('lat'))
        c.lng = _parse_coord(request.POST.get('lng'))

        lat = _parse_coord(request.POST.get('lat'))
        lng = _parse_coord(request.POST.get('lng'))

        if lat is not None and lng is not None:
            c.lat = lat
            c.lng = lng
            c.geocode_source = "manual"
            c.geocoded_at = timezone.now()
        elif c.direccion:
            # opcional: reintentar geocodificación automática si no hay lat/lng
            pass

        if municipio_id:
            c.municipio = get_object_or_404(Municipio, pk=municipio_id)

        c.save()
        messages.success(request, 'Cliente actualizado.')
        return redirect('clientes_list')

    return render(request, 'ventas/clientes/form.html', {'c': c, 'tipos': tipos, 'municipios': municipios})

@login_required
def clientes_eliminar(request, pk):
    c = get_object_or_404(Receptor_fe, pk=pk)
    if request.method == 'POST':
        c.delete()
        messages.success(request, 'Cliente eliminado.')
        return redirect('clientes_list')
    return render(request, 'ventas/clientes/eliminar.html', {'c': c})

# ---------- CATÁLOGO ----------
@login_required
def catalogo_productos(request):
    q = (request.GET.get('q') or '').strip()
    receptor_id = request.GET.get('receptor_id') or ''
    productos = Producto.objects.all()
    if q:
        productos = productos.filter(
            Q(codigo__icontains=q) | Q(descripcion__icontains=q) | Q(nombre__icontains=q)
        )

    context = {
        "q": q,
        "productos": productos,
        "receptores": Receptor_fe.objects.values("id","num_documento","nombre"),
        "receptor_actual": receptor_id,
    }
    return render(request, "ventas/catalogo.html", context)

# ---------- CARRITO por cliente (session) ----------
def _cart_key(receptor_id: int) -> str:
    return f'cart:{receptor_id}'

@login_required
def carrito_ver(request):
    """Pantalla del carrito (elige cliente, agrega productos, edita cantidades)."""
    rid = request.GET.get("receptor_id") or ""
    receptor = _ensure_receptor(rid)
    cart = _get_cart(request)
    items = []
    total = Decimal("0.00")
    if receptor:
        bucket = cart.get(str(receptor.id), {})
        # cargar datos “vivos” del producto (nombre / precio si no lo guardaste)
        for pid, row in bucket.items():
            try:
                p = Producto.objects.get(id=pid)
            except Producto.DoesNotExist:
                continue
            qty = int(row.get("qty", 1))
            precio = Decimal(str(row.get("precio"))) if row.get("precio") not in (None, "") else Decimal(str(p.preunitario or "0"))
            iva_on = bool(row.get("iva_on", False))
            desc = Decimal(str(row.get("desc_pct", "0")))
            base = (precio * qty)
            mto_desc = (base * (desc/Decimal("100"))).quantize(Decimal("0.01"))
            base_neta = base - mto_desc
            iva = (base_neta * Decimal("0.13")).quantize(Decimal("0.01")) if iva_on else Decimal("0.00")
            linea = (base_neta + iva).quantize(Decimal("0.01"))

            items.append({
                "id": p.id, "codigo": p.codigo, "nombre": p.descripcion,
                "qty": qty, "precio": f"{precio:.2f}", "iva_on": iva_on, "desc_pct": f"{desc:.2f}",
                "total": f"{linea:.2f}"
            })
            total += linea

    context = {
        "receptores": Receptor_fe.objects.values("id", "num_documento", "nombre"),
        "receptor_actual": receptor.id if receptor else "",
        "items": items,
        "total": f"{total:.2f}",
    }
    return render(request, "ventas/carrito/carrito.html", context)

@login_required
@require_POST
def carrito_agregar(request):
    """Agrega (o aumenta) un producto para el receptor dado."""
    rid = request.POST.get("receptor_id")
    pid = request.POST.get("producto_id")
    qty = int(request.POST.get("cantidad") or "1")
    precio = request.POST.get("precio")  # opcional (si lo dejas vacío, usamos preunitario)
    iva_on = request.POST.get("iva_on") in ("1","true","True","on")
    desc_pct = request.POST.get("desc_pct") or "0"

    receptor = _ensure_receptor(rid)
    if not receptor:
        return HttpResponseBadRequest("Debe seleccionar un cliente válido.")
    prod = get_object_or_404(Producto, id=pid)

    cart = _get_cart(request)
    bucket = cart.setdefault(str(receptor.id), {})
    row = bucket.setdefault(str(prod.id), {"qty": 0, "precio": None, "iva_on": False, "desc_pct": "0"})
    row["qty"] = max(1, int(row["qty"]) + max(1, qty))
    row["precio"] = precio if precio not in (None, "") else str(prod.preunitario or "0")
    row["iva_on"] = bool(iva_on)
    row["desc_pct"] = desc_pct
    _save_cart(request, cart)

    return JsonResponse({"ok": True})

@login_required
@require_POST
def carrito_actualizar(request):
    """Actualiza cantidad / precio / iva / descuento."""
    rid = request.POST.get("receptor_id")
    pid = request.POST.get("producto_id")
    receptor = _ensure_receptor(rid)
    if not receptor:
        return HttpResponseBadRequest("Cliente inválido")

    cart = _get_cart(request)
    bucket = cart.get(str(receptor.id), {})
    if pid not in bucket:
        return HttpResponseBadRequest("Producto no está en el carrito")

    row = bucket[pid]
    if "cantidad" in request.POST:
        row["qty"] = max(1, int(request.POST.get("cantidad")))
    if "precio" in request.POST and request.POST.get("precio") != "":
        row["precio"] = str(Decimal(str(request.POST.get("precio"))).quantize(Decimal("0.01")))
    if "iva_on" in request.POST:
        row["iva_on"] = request.POST.get("iva_on") in ("1","true","True","on")
    if "desc_pct" in request.POST:
        row["desc_pct"] = str(max(Decimal("0"), min(Decimal("100"), Decimal(str(request.POST.get("desc_pct"))))))
    _save_cart(request, cart)
    return JsonResponse({"ok": True})

@login_required
@require_POST
def carrito_quitar(request):
    rid = request.POST.get("receptor_id")
    pid = request.POST.get("producto_id")
    receptor = _ensure_receptor(rid)
    if not receptor:
        return HttpResponseBadRequest("Cliente inválido")
    cart = _get_cart(request)
    bucket = cart.get(str(receptor.id), {})
    bucket.pop(str(pid), None)
    _save_cart(request, cart)
    return JsonResponse({"ok": True})

@login_required
@require_POST
def carrito_vaciar(request):
    rid = request.POST.get("receptor_id")
    receptor = _ensure_receptor(rid)
    if not receptor:
        return HttpResponseBadRequest("Cliente inválido")
    cart = _get_cart(request)
    cart[str(receptor.id)] = {}
    _save_cart(request, cart)
    return JsonResponse({"ok": True})

@login_required
def carrito_cotizacion(request, receptor_id: int):
    # Renderiza una "prefactura" (no DTE, no firma)
    key = _cart_key(receptor_id)
    carro = request.session.get(key, {})
    if not carro:
        messages.error(request, 'El carrito está vacío.')
        return redirect('carrito_ver', receptor_id=receptor_id)
    receptor = get_object_or_404(Receptor_fe, pk=receptor_id)
    ids = [int(pid) for pid in carro.keys()]
    productos = Producto.objects.filter(id__in=ids)
    items, total = [], Decimal('0.00')
    for p in productos:
        cant = int(carro[str(p.id)])
        precio = (p.preunitario or Decimal('0.00'))
        linea = (precio * Decimal(cant)).quantize(Decimal('0.01'))
        total += linea
        items.append({'producto': p, 'cantidad': cant, 'precio': precio, 'total': linea})
    return render(request, 'ventas/carrito/cotizacion.html', {
        'receptor': receptor,
        'items': items,
        'total': total.quantize(Decimal('0.01'))
    })


@login_required
@require_POST
def carrito_facturar(request):
    rid = request.POST.get("receptor_id")
    receptor = _ensure_receptor(rid)
    if not receptor:
        return HttpResponseBadRequest("Debe seleccionar un cliente válido.")

    cart = _get_cart(request)
    bucket = cart.get(str(receptor.id), {})
    if not bucket:
        return HttpResponseBadRequest("Tu carrito está vacío.")

    items = []
    for pid, row in bucket.items():
        try:
            prod = Producto.objects.get(id=pid)
        except Producto.DoesNotExist:
            continue
        items.append({
            "id": prod.id,
            "codigo": prod.codigo,
            "nombre": prod.descripcion,
            "precio": float(row.get("precio") or prod.preunitario or 0),
            "cantidad": int(row.get("qty") or 1),
            "desc_pct": float(row.get("desc_pct") or 0),
            "iva_on": bool(row.get("iva_on")),
        })

    if not items:
        return HttpResponseBadRequest("Tu carrito está vacío.")

    request.session["facturacion_prefill"] = {
        "receptor_id": receptor.id,
        "items": items,
    }
    request.session.modified = True

    return redirect("/fe/generar/?from_cart=1")


@login_required
def carrito_add_go(request):
    """GET /carrito/add-go/?rid=&pid=&qty=  -> agrega y redirige al carrito."""
    rid = request.GET.get("rid")
    pid = request.GET.get("pid")
    qty = int(request.GET.get("qty") or "1")
    receptor = _ensure_receptor(rid)
    if not receptor:
        return HttpResponseBadRequest("Cliente inválido")
    prod = get_object_or_404(Producto, id=pid)
    cart = _get_cart(request)
    bucket = cart.setdefault(str(receptor.id), {})
    row = bucket.setdefault(str(prod.id), {"qty": 0, "precio": str(prod.preunitario or "0"), "iva_on": False, "desc_pct": "0"})
    row["qty"] = max(1, int(row["qty"]) + max(1, qty))
    _save_cart(request, cart)
    from django.urls import reverse
    return redirect(f'{reverse("carrito_ver")}?receptor_id={receptor.id}')

# ---------- LISTA/DETALLE VENTAS ---------
@login_required
def ventas_list(request):
    qs = FacturaElectronica.objects.select_related(
        'dtereceptor__municipio__departamento',
        'tipo_dte'
    ).all().order_by('-fecha_emision', '-id')

    # --- FILTROS ---
    tipo = request.GET.get('tipo', '')
    cliente = request.GET.get('cliente', '')
    producto = request.GET.get('producto', '')
    usuario = request.GET.get('usuario', '')
    fecha_ini = request.GET.get('fecha_ini', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    estado = request.GET.get('estado', '')
    departamento = request.GET.get('departamento', '')
    municipio = request.GET.get('municipio', '')
    monto_min = request.GET.get('monto_min', '')
    monto_max = request.GET.get('monto_max', '')

    if tipo:
        qs = qs.filter(tipo_dte__codigo=tipo)
    if cliente:
        qs = qs.filter(dtereceptor__id=cliente)
    if fecha_ini:
        qs = qs.filter(fecha_emision__gte=fecha_ini)
    if fecha_fin:
        qs = qs.filter(fecha_emision__lte=fecha_fin)
    if estado == "firmado":
        qs = qs.filter(firmado=True, recibido_mh=False)
    elif estado == "recibido":
        qs = qs.filter(recibido_mh=True)
    elif estado == "borrador":
        qs = qs.filter(firmado=False)

    if departamento:
        qs = qs.filter(dtereceptor__municipio__departamento__id=departamento)
    if municipio:
        qs = qs.filter(dtereceptor__municipio__id=municipio)

    if monto_min:
        qs = qs.filter(total_pagar__gte=monto_min)
    if monto_max:
        qs = qs.filter(total_pagar__lte=monto_max)

    if producto:
        qs = qs.filter(detalles__producto__id=producto).distinct()

    if usuario:
        qs = qs.filter(json_original__user_id=usuario)  # ⚠️ ajusta si tienes un campo real "usuario"
        # si guardas el usuario en otro campo de FacturaElectronica cámbialo aquí

    # --- PAGINACIÓN ---
    paginator = Paginator(qs, 20)
    page = request.GET.get('page')
    ventas_page = paginator.get_page(page)

    # --- Limpieza del querystring (para paginación) ---
    params = request.GET.copy()
    if "page" in params:
        params.pop("page")
    querystring = params.urlencode()

    # --- RESUMEN ---
    resumen = qs.aggregate(
        total_ventas=Sum('total_pagar'),
        cantidad=Count('id')
    )

    context = {
        'ventas': ventas_page,
        'resumen': resumen,
        'tipo': tipo,
        'cliente': cliente,
        'producto': producto,
        'usuario': usuario,
        'fecha_ini': fecha_ini,
        'fecha_fin': fecha_fin,
        'estado': estado,
        'departamento': departamento,
        'municipio': municipio,
        'monto_min': monto_min,
        'monto_max': monto_max,

        # listas para selects
        'clientes': Receptor_fe.objects.all().order_by('nombre'),
        'productos': Producto.objects.all().order_by('descripcion'),
        'usuarios': User.objects.all().order_by('username'),
        **request.GET.dict(),
        'querystring': querystring,
    }
    return render(request, 'ventas/lista.html', context)

@login_required
def venta_detalle(request, factura_id: int):
    # Reusa tu template existente del detalle
    return redirect('detalle_factura', factura_id=factura_id)

# ---------- DEVOLUCIONES DE VENTA ----------
@login_required
def devoluciones_list(request):
    devs = DevolucionVenta.objects.select_related().all().order_by('-fecha')
    return render(request, 'ventas/devoluciones/lista.html', {'devoluciones': devs})

@transaction.atomic
def devolucion_crear(request, factura_id: int):
    factura = get_object_or_404(FacturaElectronica.objects.prefetch_related('detalles__producto'), pk=factura_id)
    if request.method == 'POST':
        motivo = request.POST.get('motivo') or 'Devolución de venta'
        usuario = request.user.username if request.user.is_authenticated else None
        devolucion = DevolucionVenta.objects.create(
            num_factura=factura.numero_control or f'FAC-{factura.id}',
            motivo=motivo,
            estado='Aprobada',
            usuario=usuario
        )
        # Recoger cantidades a devolver por línea
        for det in factura.detalles.all():
            cant = int(request.POST.get(f'cant_{det.id}', 0) or 0)
            if cant <= 0:
                continue
            # Crear detalle de devolución
            DetalleDevolucionVenta.objects.create(
                devolucion=devolucion,
                producto=det.producto,
                cantidad=cant,
                motivo_detalle=motivo
            )
            # Movimiento de inventario (Entrada) — EL STOCK SE AJUSTA EN EL SIGNAL
            almacen = det.producto.almacenes.first() if det.producto.almacenes.exists() else Almacen.objects.first()
            MovimientoInventario.objects.create(
                producto=det.producto,
                almacen=almacen,
                tipo='Entrada',
                cantidad=cant,
                referencia=f'Devolución Factura {factura.codigo_generacion or factura.id}'
            )
        messages.success(request, 'Devolución registrada.')
        return redirect('devoluciones_list')

    return render(request, 'ventas/devoluciones/form.html', {'factura': factura})



# FE/views.py  (o donde tengas las vistas de facturación)
from django.http import JsonResponse
from django.db.models import Q
from INVENTARIO.models import Producto

@login_required
def api_productos(request):
    """
    Devuelve productos en JSON para el catálogo del modal.
    Parámetros:
      - q: texto de búsqueda (código o descripción)
      - page: página (1 por defecto)
      - page_size: tamaño de página (24 por defecto)
    """
    q = (request.GET.get('q') or '').strip()
    try:
        page = max(1, int(request.GET.get('page', 1)))
    except ValueError:
        page = 1
    try:
        page_size = max(1, min(96, int(request.GET.get('page_size', 24))))
    except ValueError:
        page_size = 24

    qs = Producto.objects.all().order_by('descripcion')
    if q:
        qs = qs.filter(Q(descripcion__icontains=q) | Q(codigo__icontains=q))

    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size

    results = []
    for p in qs[start:end]:
        results.append({
            'id': p.id,
            'codigo': p.codigo,
            'nombre': p.descripcion,
            'precio': str(p.precio_venta),
            'stock': p.stock,
            'imagen': (p.imagen.url if getattr(p, 'imagen', None) else ''),
            'con_iva': bool(getattr(p, 'precio_iva', False)),
        })

    return JsonResponse({
        'results': results,
        'page': page,
        'has_next': end < total,
        'total': total,
    })

#################################
# VISTA NUEVA PARA GENERAR FACTURAS

@login_required
def generar_factura(request):

    print ("Generando factura...", request)

    # variables globales arays
    productos_ids_r = []
    productos_cant_r = []
    documentos_relacionador = []
    descuentos_r = []
    precios_r = []

    #contador de intentos en session
    if 'intentos' not in request.session:
        request.session['intentos'] = 0
    
    # metodo get para cargar la vista
    if request.method == 'GET':
        # cargar datos de productos
        productos = Producto.objects.all().order_by('descripcion')
        # cargar datos de clientes
        clientes = Receptor_fe.objects.all().order_by('nombre')
        # cargar datos de tipos de documento
        tipos_documento = TiposDocIDReceptor.objects.all().order_by('descripcion')
        # cargar datos de municipios
        municipios = Municipio.objects.select_related('departamento').order_by('descripcion')
        # cargar datos de unidades de medida
        unidades_medida = TipoUnidadMedida.objects.all().order_by('descripcion')
        # cargar datos de tributos
        tributos = Tributo.objects.all().order_by('descripcion')
        # cargar datos de tipos de documento (DTE)
        tipos_dte = Tipo_dte.objects.all().order_by('descripcion')
        # cargar datos de modelos de facturacion
        modelos_facturacion = Modelofacturacion.objects.all().order_by('descripcion')
        # cargar datos de tipos de transmision
        tipos_transmision = TipoTransmision.objects.all().order_by('descripcion')

        tipos_dte = Tipo_dte.obj
        emisor_obj = None
        if emisor_obj:
            new_num_control = NumeroControl.preview_numero_control(emisor_obj)



    return render(request, 'ventas/generar_factura.html')
