from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db import transaction
from .models import DetalleCompra, DetalleDevolucionCompra, Producto, MovimientoInventario, Compra, DevolucionVenta, DevolucionCompra, Categoria, ProductoProveedor, Proveedor, TipoItem, TipoUnidadMedida, UnidadMedida, Impuesto, Almacen
from django.apps import apps
from django.db.models import Q, F, Sum

# -------- Helpers --------
def _to_decimal(val: str) -> Decimal:
    try:
        return Decimal((val or '0').replace(',', '.'))
    except (InvalidOperation, AttributeError):
        return Decimal('0')

def _recalcular_totales_y_guardar(compra: Compra):
    total = Decimal('0')
    for d in compra.detalles.all():
        total += (d.subtotal + d.iva_item)
    compra.total = total.quantize(Decimal('0.01'))
    compra.save(update_fields=['total'])

def _comprado_por_producto(compra: Compra):
    """dict {producto_id: cantidad_total_comprada}"""
    agg = (compra.detalles
           .values('producto_id')
           .annotate(c=Sum('cantidad')))
    return {r['producto_id']: r['c'] or 0 for r in agg}

def _devuelto_aprobado_por_producto(compra: Compra):
    """dict {producto_id: cantidad_total_devuelta_aprobada}"""
    agg = (DevolucionCompra.objects.filter(compra=compra, estado='Aprobada')
           .values('detalles__producto_id')
           .annotate(c=Sum('detalles__cantidad')))
    out = {}
    for r in agg:
        pid = r['detalles__producto_id']
        if pid is None:
            continue
        out[pid] = r['c'] or 0
    return out

def _es_devolucion_total(compra: Compra):
    comprado = _comprado_por_producto(compra)
    devuelto = _devuelto_aprobado_por_producto(compra)
    if not comprado:
        return False
    for pid, cant in comprado.items():
        if devuelto.get(pid, 0) < cant:
            return False
    return True
    
def inv_home(request):
    stats = {
        'productos': Producto.objects.count(),
        'categorias': Categoria.objects.count(),
        'tipos_um': TipoUnidadMedida.objects.count(),
        'impuestos': Impuesto.objects.count(),
        'almacenes': Almacen.objects.count(),
        'movs': MovimientoInventario.objects.count(),
    }
    low_stock = (Producto.objects
                 .filter(stock__lte=F('stock_minimo'))
                 .order_by('stock', 'descripcion')[:8])

    ctx = {'stats': stats, 'low_stock': low_stock}
    return render(request, 'inventario/home.html', ctx)


################################################################
# VISTAS PARA GESTIÓN DE PROVEEDORES

# Modelos de la app FE (referenciados por Proveedor)
TiposDocIDReceptor = apps.get_model('FE', 'TiposDocIDReceptor')
ActividadEconomica = apps.get_model('FE', 'ActividadEconomica')
Departamento = apps.get_model('FE', 'Departamento')
Municipio = apps.get_model('FE', 'Municipio')

# ---------- Proveedores ----------
def listar_proveedores(request):
    q = (request.GET.get('q') or '').strip()
    depto_id = request.GET.get('depto') or ''
    muni_id = request.GET.get('muni') or ''
    act_id = request.GET.get('act') or ''

    proveedores = Proveedor.objects.select_related('departamento', 'municipio').all()

    if q:
        proveedores = proveedores.filter(
            Q(nombre__icontains=q) | Q(num_documento__icontains=q) | Q(contacto__icontains=q)
        )
    if depto_id:
        proveedores = proveedores.filter(departamento_id=depto_id)
    if muni_id:
        proveedores = proveedores.filter(municipio_id=muni_id)
    if act_id:
        proveedores = proveedores.filter(actividades_economicas__id=act_id)

    proveedores = proveedores.order_by('nombre').distinct()

    paginator = Paginator(proveedores, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'proveedores': page_obj,
        'q': q,
        'departamentos': Departamento.objects.all().order_by('descripcion'),
        'municipios': Municipio.objects.filter(departamento_id=depto_id).order_by('descripcion') if depto_id else [],
        'actividades': ActividadEconomica.objects.all().order_by('descripcion'),
        'f_depto': depto_id, 'f_muni': muni_id, 'f_act': act_id,
    }
    return render(request, 'proveedores/lista.html', ctx)

def crear_proveedor(request):
    from django.contrib import messages as flash
    if request.method == 'POST':
        nombre = request.POST.get('nombre') or ''
        num_documento = request.POST.get('num_documento') or ''
        tipo_doc_id = request.POST.get('tipo_documento') or None
        depto_id = request.POST.get('departamento') or None
        muni_id = request.POST.get('municipio') or None
        contacto = request.POST.get('contacto') or ''
        telefono = request.POST.get('telefono') or ''
        email = request.POST.get('email') or ''
        direccion = request.POST.get('direccion') or ''
        condiciones_pago = request.POST.get('condiciones_pago') or ''

        if not nombre or not num_documento:
            messages.error(request, 'Nombre y número de documento son obligatorios.')
            return redirect('proveedores-crear')

        prov = Proveedor.objects.create(
            nombre=nombre,
            num_documento=num_documento,
            tipo_documento_id=tipo_doc_id if tipo_doc_id else None,
            departamento_id=depto_id if depto_id else None,
            municipio_id=muni_id if muni_id else None,
            contacto=contacto,
            telefono=telefono,
            email=email,
            direccion=direccion,
            condiciones_pago=condiciones_pago,
        )

        act_ids = request.POST.getlist('actividades_economicas')
        if act_ids:
            prov.actividades_economicas.set(act_ids)

        flash.success(request, 'Proveedor creado correctamente.')
        return redirect('proveedores-detalle', pk=prov.pk)

    ctx = {
        'tipos_doc': TiposDocIDReceptor.objects.all().order_by('descripcion'),
        'departamentos': Departamento.objects.all().order_by('descripcion'),
        'municipios': [],  # se cargan por ajax tras seleccionar depto
        'actividades': ActividadEconomica.objects.all().order_by('descripcion'),
    }
    return render(request, 'proveedores/formulario.html', ctx)

def editar_proveedor(request, pk):
    from django.contrib import messages as flash
    prov = get_object_or_404(Proveedor, pk=pk)

    if request.method == 'POST':
        prov.nombre = request.POST.get('nombre') or prov.nombre
        prov.num_documento = request.POST.get('num_documento') or prov.num_documento
        prov.tipo_documento_id = request.POST.get('tipo_documento') or None
        prov.departamento_id = request.POST.get('departamento') or None
        prov.municipio_id = request.POST.get('municipio') or None
        prov.contacto = request.POST.get('contacto') or ''
        prov.telefono = request.POST.get('telefono') or ''
        prov.email = request.POST.get('email') or ''
        prov.direccion = request.POST.get('direccion') or ''
        prov.condiciones_pago = request.POST.get('condiciones_pago') or ''
        prov.save()

        act_ids = request.POST.getlist('actividades_economicas')
        prov.actividades_economicas.set(act_ids)

        flash.success(request, 'Proveedor actualizado.')
        return redirect('proveedores-detalle', pk=prov.pk)

    ctx = {
        'proveedor': prov,
        'tipos_doc': TiposDocIDReceptor.objects.all().order_by('descripcion'),
        'departamentos': Departamento.objects.all().order_by('descripcion'),
        'municipios': Municipio.objects.filter(departamento_id=prov.departamento_id).order_by('descripcion') if prov.departamento_id else [],
        'actividades': ActividadEconomica.objects.all().order_by('descripcion'),
    }
    return render(request, 'proveedores/formulario.html', ctx)

def eliminar_proveedor(request, pk):
    prov = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        prov.delete()
        messages.success(request, 'Proveedor eliminado.')
        return redirect('proveedores-lista')
    return render(request, 'proveedores/confirmar_eliminar.html', {'proveedor': prov})

def detalle_proveedor(request, pk):
    prov = get_object_or_404(Proveedor, pk=pk)
    productos = ProductoProveedor.objects.filter(proveedor_id=prov.pk).select_related('unidad_medida', 'tipo_item').order_by('descripcion')
    ctx = {'proveedor': prov, 'productos': productos}
    return render(request, 'proveedores/detalle.html', ctx)

# ---------- ProductoProveedor ----------
def crear_producto_proveedor(request, proveedor_id):
    prov = get_object_or_404(Proveedor, pk=proveedor_id)

    if request.method == 'POST':
        codigo = request.POST.get('codigo') or ''
        descripcion = request.POST.get('descripcion') or ''
        unidad_id = request.POST.get('unidad_medida') or None
        tipo_item_id = request.POST.get('tipo_item') or None
        preunitario = request.POST.get('preunitario') or '0'
        referencia_interna = request.POST.get('referencia_interna') or ''
        fecha_vencimiento = request.POST.get('fecha_vencimiento') or None
        imagen = request.FILES.get('imagen')

        if not codigo or not descripcion:
            messages.error(request, 'Código y descripción son obligatorios.')
            return redirect('prov-prod-crear', proveedor_id=proveedor_id)

        ProductoProveedor.objects.create(
            proveedor=prov,
            codigo=codigo,
            descripcion=descripcion,
            unidad_medida_id=unidad_id,
            preunitario=Decimal(preunitario or '0'),
            tipo_item_id=tipo_item_id,
            referencia_interna=referencia_interna or None,
            fecha_vencimiento=fecha_vencimiento or None,
            imagen=imagen
        )
        messages.success(request, 'Producto agregado al proveedor.')
        return redirect('proveedores-detalle', pk=proveedor_id)

    ctx = {
        'proveedor': prov,
        'unidades': TipoUnidadMedida.objects.all().order_by('descripcion') if hasattr(TipoUnidadMedida, 'descripcion') else TipoUnidadMedida.objects.all().order_by('nombre'),
        'tipos_item': TipoItem.objects.all().order_by('descripcion'),
    }
    return render(request, 'proveedores/producto_form.html', ctx)

def editar_producto_proveedor(request, proveedor_id, pk):
    prov = get_object_or_404(Proveedor, pk=proveedor_id)
    prod = get_object_or_404(ProductoProveedor, pk=pk, proveedor=prov)

    if request.method == 'POST':
        prod.codigo = request.POST.get('codigo') or prod.codigo
        prod.descripcion = request.POST.get('descripcion') or prod.descripcion
        prod.unidad_medida_id = request.POST.get('unidad_medida') or None
        prod.tipo_item_id = request.POST.get('tipo_item') or None
        pre = request.POST.get('preunitario') or None
        if pre is not None:
            try:
                prod.preunitario = Decimal(pre)
            except Exception:
                pass
        prod.referencia_interna = request.POST.get('referencia_interna') or None
        prod.fecha_vencimiento = request.POST.get('fecha_vencimiento') or None
        if request.FILES.get('imagen'):
            prod.imagen = request.FILES['imagen']
        prod.save()
        messages.success(request, 'Producto de proveedor actualizado.')
        return redirect('proveedores-detalle', pk=proveedor_id)

    ctx = {
        'proveedor': prov,
        'producto': prod,
        'unidades': TipoUnidadMedida.objects.all().order_by('descripcion') if hasattr(TipoUnidadMedida, 'descripcion') else TipoUnidadMedida.objects.all().order_by('nombre'),
        'tipos_item': TipoItem.objects.all().order_by('descripcion'),
    }
    return render(request, 'proveedores/producto_form.html', ctx)

def eliminar_producto_proveedor(request, proveedor_id, pk):
    prov = get_object_or_404(Proveedor, pk=proveedor_id)
    prod = get_object_or_404(ProductoProveedor, pk=pk, proveedor=prov)
    if request.method == 'POST':
        prod.delete()
        messages.success(request, 'Producto de proveedor eliminado.')
        return redirect('proveedores-detalle', pk=proveedor_id)
    return render(request, 'proveedores/producto_confirmar_eliminar.html', {'proveedor': prov, 'producto': prod})

# ---------- AJAX: Municipios por Departamento ----------
def municipios_por_departamento(request):
    depto_id = request.GET.get('depto')
    data = []
    if depto_id:
        # Devolver 'descripcion' (no 'nombre')
        data = list(Municipio.objects
                    .filter(departamento_id=depto_id)
                    .order_by('descripcion')
                    .values('id', 'descripcion'))
    return JsonResponse({'municipios': data})

################################################################
# VISTAS PARA GESTIÓN DE COMPRAS

def _recalcular_totales_y_guardar(compra: Compra):
    total = Decimal('0')
    for d in compra.detalles.all():
        total += (d.subtotal + d.iva_item)
    compra.total = total.quantize(Decimal('0.01'))
    compra.save(update_fields=['total'])
    
# Listar compras
def listar_compras(request):
    qs = Compra.objects.select_related('proveedor').order_by('-fecha')
    prov = request.GET.get('proveedor')
    estado = request.GET.get('estado')
    q = (request.GET.get('q') or '').strip()

    if prov:
        qs = qs.filter(proveedor_id=prov)
    if estado:
        qs = qs.filter(estado=estado)
    if q:
        qs = qs.filter(Q(numero_documento__icontains=q) | Q(proveedor__nombre__icontains=q))

    context = {
        'compras': qs,
        'proveedores': Proveedor.objects.all().order_by('nombre'),
        'f_proveedor': prov or '',
        'f_estado': estado or '',
        'q': q,
    }
    return render(request, 'compras/lista.html', context)

# Crear compra sin forms.py
@transaction.atomic
def crear_compra(request):
    proveedores = Proveedor.objects.all().order_by('nombre')
    productos = Producto.objects.all().order_by('descripcion')
    almacenes = Almacen.objects.all().order_by('nombre')  # lo pedías en el form
    tipo_compra_choices = DetalleCompra.TIPO_COMPRA_CHOICES

    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        almacen_id = request.POST.get('almacen')  # si quieres usarlo en referencia
        numero_doc = request.POST.get('numero_documento') or ''
        tipo_doc = request.POST.get('tipo_documento') or ''

        if not proveedor_id:
            messages.error(request, 'Proveedor es obligatorio.')
            return redirect('compras-crear')

        compra = Compra.objects.create(
            proveedor_id=proveedor_id,
            numero_documento=numero_doc,
            tipo_documento=tipo_doc,
        )

        prod_ids = request.POST.getlist('producto')
        cants    = request.POST.getlist('cantidad')
        precios  = request.POST.getlist('precio_unitario')
        tipos    = request.POST.getlist('tipo_compra')

        for i in range(len(prod_ids)):
            pid = prod_ids[i]
            if not pid:
                continue
            cantidad = int(cants[i] or 0)
            precio   = _to_decimal(precios[i])
            tipo     = (tipos[i] or 'GR_INT')
            if cantidad <= 0 or precio <= 0:
                continue

            prod = get_object_or_404(Producto, pk=pid)
            det = DetalleCompra.objects.create(
                compra=compra,
                producto=prod,
                cantidad=cantidad,
                precio_unitario=precio,
                tipo_compra=tipo,
            )
            # Mantener último costo
            Producto.objects.filter(pk=prod.pk).update(precio_compra=precio)
            # NO tocar stock aquí; el signal de DetalleCompra crea Movimiento "Entrada"

        _recalcular_totales_y_guardar(compra)
        messages.success(request, f'Compra #{compra.id} creada.')
        return redirect('compras-detalle', pk=compra.pk)

    ctx = {
        'proveedores': proveedores,
        'productos': productos,
        'almacenes': almacenes,
        'tipo_compra_choices': tipo_compra_choices,
    }
    return render(request, 'compras/formulario.html', ctx)

# -------- Detalle --------
def detalle_compra(request, pk):
    compra = get_object_or_404(
        Compra.objects.select_related('proveedor').prefetch_related('detalles__producto'),
        pk=pk
    )
    # totales
    tot_sub = compra.detalles.aggregate(s=Sum('subtotal'))['s'] or Decimal('0')
    tot_iva = compra.detalles.aggregate(s=Sum('iva_item'))['s'] or Decimal('0')
    return render(request, 'compras/detalle.html', {
        'compra': compra,
        'tot_sub': tot_sub,
        'tot_iva': tot_iva,
        'tot_total': (tot_sub + tot_iva),
    })

# -------- Editar (reemplaza completamente los ítems) --------
@transaction.atomic
def editar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)

    proveedores = Proveedor.objects.all().order_by('nombre')
    productos = Producto.objects.all().order_by('descripcion')
    almacenes = Almacen.objects.all().order_by('nombre')
    tipo_compra_choices = DetalleCompra.TIPO_COMPRA_CHOICES

    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        if proveedor_id:
            compra.proveedor_id = proveedor_id
            compra.save(update_fields=['proveedor'])

        # 1) Borrar movimientos de esta compra (revertirá stock via pre_delete de Movimiento)
        ref_prefix = f'Compra #{compra.id}'
        MovimientoInventario.objects.filter(referencia__startswith=ref_prefix).delete()
        # 2) Borrar detalles
        compra.detalles.all().delete()

        # 3) Crear detalles nuevos
        prod_ids = request.POST.getlist('producto')
        cants    = request.POST.getlist('cantidad')
        precios  = request.POST.getlist('precio_unitario')
        tipos    = request.POST.getlist('tipo_compra')

        for i in range(len(prod_ids)):
            pid = prod_ids[i]
            if not pid:
                continue
            cantidad = int(cants[i] or 0)
            precio   = _to_decimal(precios[i])
            tipo     = (tipos[i] or 'GR_INT')
            if cantidad <= 0 or precio <= 0:
                continue

            prod = get_object_or_404(Producto, pk=pid)
            DetalleCompra.objects.create(
                compra=compra,
                producto=prod,
                cantidad=cantidad,
                precio_unitario=precio,
                tipo_compra=tipo,
            )
            Producto.objects.filter(pk=prod.pk).update(precio_compra=precio)
            # De nuevo: NO tocar stock; el signal hará la Entrada

        _recalcular_totales_y_guardar(compra)
        messages.success(request, f'Compra #{compra.id} actualizada.')
        return redirect('compras-detalle', pk=compra.pk)

    ctx = {
        'compra': compra,
        'proveedores': proveedores,
        'productos': productos,
        'almacenes': almacenes,
        'tipo_compra_choices': tipo_compra_choices,
    }
    return render(request, 'compras/formulario.html', ctx)

# -------- Eliminar --------
@transaction.atomic
def eliminar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        ref_prefix = f'Compra #{compra.id}'
        MovimientoInventario.objects.filter(referencia__startswith=ref_prefix).delete()
        compra.delete()
        messages.success(request, 'Compra eliminada.')
        return redirect('compras-lista')
    return render(request, 'compras/confirmar_eliminar.html', {'compra': compra})

# Marcar estados
@transaction.atomic
def marcar_compra_pagado(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    compra.estado = 'Pagado'
    compra.save(update_fields=['estado'])
    messages.success(request, f'Compra #{compra.id} marcada como Pagado.')
    return redirect('compras-detalle', pk=pk)

@transaction.atomic
def marcar_compra_devuelto(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if not _es_devolucion_total(compra):
        messages.error(request, 'Aún no es devolución total. Verifica cantidades.')
        return redirect('compras-detalle', pk=pk)
    compra.estado = 'Devuelto'
    compra.save(update_fields=['estado'])
    messages.success(request, f'Compra #{compra.id} marcada como Devuelto.')
    return redirect('compras-detalle', pk=pk)

################################################################
# VISTAS PARA GESTIÓN DE DEVOLUCIONES

#devoluciones de compra

def listar_devoluciones_compra(request):
    devoluciones = (DevolucionCompra.objects
                    .select_related('compra', 'compra__proveedor')
                    .order_by('-fecha'))
    return render(request, 'compras/devoluciones_compra/lista.html', {'devoluciones': devoluciones})

@transaction.atomic
def crear_devolucion_compra(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    productos = Producto.objects.filter(detallecompra__compra=compra).distinct().order_by('descripcion')

    if request.method == 'POST':
        motivo = request.POST.get('motivo') or ''
        estado = request.POST.get('estado') or 'Aprobada'  # Pendiente/Aprobada/Rechazada

        # líneas
        prod_ids = request.POST.getlist('producto')
        cants    = request.POST.getlist('cantidad')
        motivos  = request.POST.getlist('motivo_detalle')

        if not any(prod_ids):
            messages.error(request, 'Agrega al menos una línea de devolución.')
            return redirect('dev-compra-crear', compra_id=compra.id)

        dev = DevolucionCompra.objects.create(
            compra=compra,
            motivo=motivo,
            estado=estado
        )

        # Validación: no devolver más de lo comprado (acumulado con otras aprobadas)
        comprado = _comprado_por_producto(compra)
        ya_dev   = _devuelto_aprobado_por_producto(compra)

        for i in range(len(prod_ids)):
            pid = prod_ids[i]
            if not pid:
                continue
            cantidad = int(cants[i] or 0)
            if cantidad <= 0:
                continue
            motivo_det = motivos[i] if i < len(motivos) else ''

            pid_int = int(pid)
            if estado == 'Aprobada':
                limite = comprado.get(pid_int, 0) - ya_dev.get(pid_int, 0)
                if cantidad > limite:
                    messages.error(request, 'La cantidad a devolver excede lo comprado para un producto.')
                    # rollback implícito por @transaction.atomic
                    raise Exception('Cantidad de devolución inválida')

            DetalleDevolucionCompra.objects.create(
                devolucion=dev,
                producto_id=pid_int,
                cantidad=cantidad,
                motivo_detalle=motivo_det
            )
            # NO crear movimientos aquí. El signal lo hará si estado == Aprobada.

        # Si quedó en Aprobada, podemos actualizar estado de la compra si ya es total
        if estado == 'Aprobada' and _es_devolucion_total(compra):
            compra.estado = 'Devuelto'
            compra.save(update_fields=['estado'])

        messages.success(request, f'Devolución #{dev.id} creada para la compra #{compra.id}.')
        return redirect('compras-detalle', pk=compra.id)

    return render(request, 'compras/devoluciones_compra/formulario.html', {
        'compra': compra,
        'productos': productos,
    })

# devoluciones de venta

def listar_devoluciones_venta(request):
    devoluciones = DevolucionVenta.objects.all()
    return render(request, 'devoluciones_venta/lista.html', {'devoluciones': devoluciones})

# Crear devolución de venta
def crear_devolucion_venta(request):
    if request.method == 'POST':
        num_factura = request.POST.get('num_factura')
        motivo = request.POST.get('motivo')
        DevolucionVenta.objects.create(num_factura=num_factura, motivo=motivo)
        return redirect('devoluciones-venta-lista')
    return render(request, 'devoluciones_venta/formulario.html')

################################################################
# VISTAS PARA GESTIÓN DE PRODUCTOS

def productos_lista(request):
    q = (request.GET.get('q') or '').strip()
    cat_id = request.GET.get('cat') or ''
    qs = Producto.objects.select_related('categoria', 'unidad_medida').all()
    if q:
        qs = qs.filter(Q(codigo__icontains=q) | Q(descripcion__icontains=q))
    if cat_id:
        qs = qs.filter(categoria_id=cat_id)
    qs = qs.order_by('descripcion')
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))
    ctx = {
        'productos': page,
        'q': q,
        'categorias': Categoria.objects.all().order_by('nombre'),
        'f_cat': cat_id,
    }
    return render(request, 'inventario/productos/lista.html', ctx)

def productos_crear(request):
    if request.method == 'POST':
        codigo = (request.POST.get('codigo') or '').strip()
        descripcion = (request.POST.get('descripcion') or '').strip()
        categoria_id = request.POST.get('categoria') or None
        unidad_id = request.POST.get('unidad_medida') or None   # TipoUnidadMedida
        precio_compra = _to_decimal(request.POST.get('precio_compra'))
        precio_venta = _to_decimal(request.POST.get('precio_venta'))
        stock = int(request.POST.get('stock') or 0)
        stock_minimo = int(request.POST.get('stock_minimo') or 0)
        stock_maximo = int(request.POST.get('stock_maximo') or 0)
        maneja_lotes = (request.POST.get('maneja_lotes') == 'on')
        fecha_vencimiento = request.POST.get('fecha_vencimiento') or None
        imagen = request.FILES.get('imagen')
        impuestos = request.POST.getlist('impuestos')
        almacenes = request.POST.getlist('almacenes')

        if not codigo or not descripcion:
            messages.error(request, 'Código y descripción son obligatorios.')
            return redirect('inv-productos-crear')
        
        # calculo de precio unitario si no se proporciona y si hay impuestos = precio de venta + el impuesto seleccionado, si no se proporciona impuesto se toma el 1.13
        if not precio_venta and impuestos:
            impuesto = Impuesto.objects.filter(id__in=impuestos).first()
            if impuesto:
                precio_venta = precio_compra * (1 + impuesto.porcentaje / 100)
            else:
                precio_venta = precio_compra * Decimal('1.13')
        elif not precio_venta:
            precio_venta = precio_compra * Decimal('1.13')


        prod = Producto.objects.create(
            codigo=codigo,
            descripcion=descripcion,
            categoria_id=categoria_id,
            unidad_medida_id=unidad_id,
            preunitario=precio_venta,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
            stock_minimo=stock_minimo,
            stock_maximo=stock_maximo,
            maneja_lotes=maneja_lotes,
            fecha_vencimiento=fecha_vencimiento or None,
            imagen=imagen
        )
        if impuestos:
            prod.impuestos.set(impuestos)
        if almacenes:
            prod.almacenes.set(almacenes)

        messages.success(request, 'Producto creado.')
        return redirect('inv-productos-lista')

    ctx = {
        'categorias': Categoria.objects.all().order_by('nombre'),
        'tipos_um': TipoUnidadMedida.objects.all().order_by('descripcion'),
        'impuestos': Impuesto.objects.all().order_by('nombre'),
        'almacenes': Almacen.objects.all().order_by('nombre'),
    }
    return render(request, 'inventario/productos/form.html', ctx)

def productos_editar(request, pk):
    obj = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        obj.codigo = (request.POST.get('codigo') or obj.codigo).strip()
        obj.descripcion = (request.POST.get('descripcion') or obj.descripcion).strip()
        obj.categoria_id = request.POST.get('categoria') or None
        obj.unidad_medida_id = request.POST.get('unidad_medida') or None
        obj.precio_compra = _to_decimal(request.POST.get('precio_compra'))
        obj.precio_venta = _to_decimal(request.POST.get('precio_venta'))
        obj.stock = int(request.POST.get('stock') or obj.stock or 0)
        obj.stock_minimo = int(request.POST.get('stock_minimo') or 0)
        obj.stock_maximo = int(request.POST.get('stock_maximo') or 0)
        obj.maneja_lotes = (request.POST.get('maneja_lotes') == 'on')
        obj.fecha_vencimiento = request.POST.get('fecha_vencimiento') or None
        if request.FILES.get('imagen'):
            obj.imagen = request.FILES['imagen']
        obj.save()

        impuestos = request.POST.getlist('impuestos')
        obj.impuestos.set(impuestos)
        almacenes = request.POST.getlist('almacenes')
        obj.almacenes.set(almacenes)

        messages.success(request, 'Producto actualizado.')
        return redirect('inv-productos-lista')

    ctx = {
        'obj': obj,
        'categorias': Categoria.objects.all().order_by('nombre'),
        'tipos_um': TipoUnidadMedida.objects.all().order_by('descripcion'),
        'impuestos': Impuesto.objects.all().order_by('nombre'),
        'almacenes': Almacen.objects.all().order_by('nombre'),
    }
    return render(request, 'inventario/productos/form.html', ctx)

def productos_eliminar(request, pk):
    obj = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('inv-productos-lista')
    return render(request, 'inventario/commons/confirm_delete.html', {'obj': obj, 'back_url': 'inv-productos-lista'})

################################################################
# VISTAS PARA GESTIÓN DE MOVIMIENTOS DE INVENTARIO

def movimientos_lista(request):
    q = (request.GET.get('q') or '').strip()
    tipo = request.GET.get('tipo') or ''
    qs = (MovimientoInventario.objects
          .select_related('producto', 'almacen')
          .all())
    if q:
        qs = qs.filter(
            Q(producto__codigo__icontains=q) |
            Q(producto__descripcion__icontains=q) |
            Q(referencia__icontains=q)
        )
    if tipo:
        qs = qs.filter(tipo=tipo)
    qs = qs.order_by('-fecha')
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page'))
    ctx={
        'movs': page,
        'q': q,
        'f_tipo': tipo,
        'tipos': MovimientoInventario.TIPO_MOVIMIENTO,
        }
    
    return render(request,'inventario/movimientos/lista.html',ctx)

@transaction.atomic
def movimientos_crear(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        almacen_id = request.POST.get('almacen')
        tipo = request.POST.get('tipo')  # Entrada|Salida|Ajuste
        cantidad = int(request.POST.get('cantidad') or 0)
        referencia = request.POST.get('referencia') or ''

        if not producto_id or not almacen_id or not tipo or cantidad == 0:
            messages.error(request, 'Producto, almacén, tipo y cantidad son obligatorios.')
            return redirect('inv-movs-crear')

        # Guarda siempre cantidad positiva para Entrada/Salida.
        guardar_cant = abs(cantidad) if tipo in ('Entrada', 'Salida') else cantidad

        MovimientoInventario.objects.create(
            producto_id=producto_id,
            almacen_id=almacen_id,
            tipo=tipo,
            cantidad=guardar_cant,
            referencia=referencia
        )

        messages.success(request, 'Movimiento registrado.')
        return redirect('inv-movs-lista')

    ctx = {
        'productos': Producto.objects.all().order_by('descripcion'),
        'almacenes': Almacen.objects.all().order_by('nombre'),
        'tipos': MovimientoInventario.TIPO_MOVIMIENTO,
        'preselect_tipo': request.GET.get('tipo') or '',
    }
    return render(request, 'inventario/movimientos/form.html', ctx)

@transaction.atomic
def movimientos_editar(request, pk):
    mov = get_object_or_404(MovimientoInventario, pk=pk)
    if request.method == 'POST':
        # revertir efecto anterior
        if mov.tipo == 'Entrada':
            Producto.objects.filter(pk=mov.producto_id).update(stock=F('stock') - mov.cantidad)
        elif mov.tipo == 'Salida':
            Producto.objects.filter(pk=mov.producto_id).update(stock=F('stock') + mov.cantidad)
        elif mov.tipo == 'Ajuste':
            Producto.objects.filter(pk=mov.producto_id).update(stock=F('stock') - mov.cantidad)

        producto_id = request.POST.get('producto')
        almacen_id = request.POST.get('almacen')
        tipo = request.POST.get('tipo')
        cantidad = int(request.POST.get('cantidad') or 0)
        referencia = request.POST.get('referencia') or ''

        if not producto_id or not almacen_id or not tipo or cantidad == 0:
            messages.error(request, 'Producto, almacén, tipo y cantidad son obligatorios.')
            return redirect('inv-movs-editar', pk=mov.pk)

        mov.producto_id = producto_id
        mov.almacen_id = almacen_id
        mov.tipo = tipo
        mov.cantidad = abs(cantidad) if tipo in ('Entrada', 'Salida') else cantidad
        mov.referencia = referencia
        mov.save()

        # aplicar nuevo
        if tipo == 'Entrada':
            Producto.objects.filter(pk=producto_id).update(stock=F('stock') + abs(cantidad))
        elif tipo == 'Salida':
            Producto.objects.filter(pk=producto_id).update(stock=F('stock') - abs(cantidad))
        elif tipo == 'Ajuste':
            Producto.objects.filter(pk=producto_id).update(stock=F('stock') + cantidad)

        messages.success(request, 'Movimiento actualizado.')
        return redirect('inv-movs-lista')

    ctx = {
        'mov': mov,
        'productos': Producto.objects.all().order_by('descripcion'),
        'almacenes': Almacen.objects.all().order_by('nombre'),
        'tipos': MovimientoInventario.TIPO_MOVIMIENTO,   # <- AQUI
        'preselect_tipo': '',                            # no aplica en editar
    }
    return render(request, 'inventario/movimientos/form.html', ctx)

@transaction.atomic
def movimientos_eliminar(request, pk):
    mov = get_object_or_404(MovimientoInventario, pk=pk)
    if request.method == 'POST':
        # revertir efecto en stock
        if mov.tipo == 'Entrada':
            Producto.objects.filter(pk=mov.producto_id).update(stock=F('stock') - mov.cantidad)
        elif mov.tipo == 'Salida':
            Producto.objects.filter(pk=mov.producto_id).update(stock=F('stock') + mov.cantidad)
        elif mov.tipo == 'Ajuste':
            Producto.objects.filter(pk=mov.producto_id).update(stock=F('stock') - mov.cantidad)
        mov.delete()
        messages.success(request, 'Movimiento eliminado.')
        return redirect('inv-movs-lista')
    return render(request, 'inventario/commons/confirm_delete.html', {'obj': mov, 'back_url': 'inv-movs-lista'})

################################################################
# VISTAS PARA GESTIÓN DE CATEGORIAS    ok

def categorias_lista(request):
    q = (request.GET.get('q') or '').strip()
    qs = Categoria.objects.all()
    if q:
        qs = qs.filter(nombre__icontains=q)
    qs = qs.order_by('nombre')
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventario/categorias/lista.html', {'categorias': page, 'q': q})

def categorias_crear(request):
    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        else:
            Categoria.objects.create(nombre=nombre)
            messages.success(request, 'Categoría creada.')
            return redirect('inv-categorias-lista')
    return render(request, 'inventario/categorias/form.html')

def categorias_editar(request, pk):
    obj = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        else:
            obj.nombre = nombre
            obj.save()
            messages.success(request, 'Categoría actualizada.')
            return redirect('inv-categorias-lista')
    return render(request, 'inventario/categorias/form.html', {'obj': obj})

def categorias_eliminar(request, pk):
    obj = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Categoría eliminada.')
        return redirect('inv-categorias-lista')
    return render(request, 'inventario/commons/confirm_delete.html', {'obj': obj, 'back_url': 'inv-categorias-lista'})

################################################################
# VISTAS PARA GESTIÓN DE TIPO UNIDADES DE MEDIDA y UNIDADES DE MEDIDA ok

def tipos_um_lista(request):
    q = (request.GET.get('q') or '').strip()
    qs = TipoUnidadMedida.objects.all()
    if q:
        qs = qs.filter(Q(codigo__icontains=q) | Q(descripcion__icontains=q))
    qs = qs.order_by('codigo')
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventario/tipos_um/lista.html', {'tipos': page, 'q': q})

def tipos_um_crear(request):
    if request.method == 'POST':
        codigo = (request.POST.get('codigo') or '').strip()
        descripcion = (request.POST.get('descripcion') or '').strip()
        if not codigo or not descripcion:
            messages.error(request, 'Código y descripción son obligatorios.')
        else:
            TipoUnidadMedida.objects.create(codigo=codigo, descripcion=descripcion)
            messages.success(request, 'Tipo de unidad creado.')
            return redirect('inv-tiposum-lista')
    return render(request, 'inventario/tipos_um/form.html')

def tipos_um_editar(request, pk):
    obj = get_object_or_404(TipoUnidadMedida, pk=pk)
    if request.method == 'POST':
        codigo = (request.POST.get('codigo') or '').strip()
        descripcion = (request.POST.get('descripcion') or '').strip()
        if not codigo or not descripcion:
            messages.error(request, 'Código y descripción son obligatorios.')
        else:
            obj.codigo = codigo
            obj.descripcion = descripcion
            obj.save()
            messages.success(request, 'Tipo de unidad actualizado.')
            return redirect('inv-tiposum-lista')
    return render(request, 'inventario/tipos_um/form.html', {'obj': obj})

def tipos_um_eliminar(request, pk):
    obj = get_object_or_404(TipoUnidadMedida, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Tipo de unidad eliminado.')
        return redirect('inv-tiposum-lista')
    return render(request, 'inventario/commons/confirm_delete.html', {'obj': obj, 'back_url': 'inv-tiposum-lista'})


# ---- VISTAS PARA UNIDADES DE MEDIDA ----
def listar_unidades_medida(request):
    unidades = UnidadMedida.objects.all()
    return render(request, 'unidades_medida/lista.html', {'unidades': unidades})

def crear_unidad_medida(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        abreviatura = request.POST.get('abreviatura')
        UnidadMedida.objects.create(nombre=nombre, abreviatura=abreviatura)
        return redirect('unidades-lista')
    return render(request, 'unidades_medida/formulario.html')

def editar_unidad_medida(request, pk):
    unidad = get_object_or_404(UnidadMedida, pk=pk)
    if request.method == 'POST':
        unidad.nombre = request.POST.get('nombre')
        unidad.abreviatura = request.POST.get('abreviatura')
        unidad.save()
        return redirect('unidades-lista')
    return render(request, 'unidades_medida/formulario.html', {'unidad': unidad})

def eliminar_unidad_medida(request, pk):
    unidad = get_object_or_404(UnidadMedida, pk=pk)
    if request.method == 'POST':
        unidad.delete()
        return redirect('unidades-lista')
    return render(request, 'unidades_medida/confirmar_eliminar.html', {'unidad': unidad})

################################################################
# VISTAS PARA GESTIÓN DE IMPUESTOS

def impuestos_lista(request):
    q = (request.GET.get('q') or '').strip()
    qs = Impuesto.objects.all()
    if q:
        qs = qs.filter(Q(nombre__icontains=q))
    qs = qs.order_by('nombre')
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventario/impuestos/lista.html', {'impuestos': page, 'q': q})

def impuestos_crear(request):
    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        porcentaje = _to_decimal(request.POST.get('porcentaje'))
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        else:
            Impuesto.objects.create(nombre=nombre, porcentaje=porcentaje)
            messages.success(request, 'Impuesto creado.')
            return redirect('inv-impuestos-lista')
    return render(request, 'inventario/impuestos/form.html')

def impuestos_editar(request, pk):
    obj = get_object_or_404(Impuesto, pk=pk)
    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        porcentaje = _to_decimal(request.POST.get('porcentaje'))
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        else:
            obj.nombre = nombre
            obj.porcentaje = porcentaje
            obj.save()
            messages.success(request, 'Impuesto actualizado.')
            return redirect('inv-impuestos-lista')
    return render(request, 'inventario/impuestos/form.html', {'obj': obj})

def impuestos_eliminar(request, pk):
    obj = get_object_or_404(Impuesto, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Impuesto eliminado.')
        return redirect('inv-impuestos-lista')
    return render(request, 'inventario/commons/confirm_delete.html', {'obj': obj, 'back_url': 'inv-impuestos-lista'})


################################################################
# VISTAS PARA GESTIÓN DE ALMACENES

def almacenes_lista(request):
    q = (request.GET.get('q') or '').strip()
    qs = Almacen.objects.all()
    if q:
        qs = qs.filter(Q(nombre__icontains=q) | Q(ubicacion__icontains=q) | Q(responsable__icontains=q))
    qs = qs.order_by('nombre')
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'inventario/almacenes/lista.html', {'almacenes': page, 'q': q})

def almacenes_crear(request):
    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        ubicacion = (request.POST.get('ubicacion') or '').strip()
        responsable = (request.POST.get('responsable') or '').strip()
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        else:
            Almacen.objects.create(nombre=nombre, ubicacion=ubicacion or None, responsable=responsable or None)
            messages.success(request, 'Almacén creado.')
            return redirect('inv-almacenes-lista')
    return render(request, 'inventario/almacenes/form.html')

def almacenes_editar(request, pk):
    obj = get_object_or_404(Almacen, pk=pk)
    if request.method == 'POST':
        obj.nombre = (request.POST.get('nombre') or '').strip()
        obj.ubicacion = (request.POST.get('ubicacion') or '').strip() or None
        obj.responsable = (request.POST.get('responsable') or '').strip() or None
        if not obj.nombre:
            messages.error(request, 'El nombre es obligatorio.')
        else:
            obj.save()
            messages.success(request, 'Almacén actualizado.')
            return redirect('inv-almacenes-lista')
    return render(request, 'inventario/almacenes/form.html', {'obj': obj})

def almacenes_eliminar(request, pk):
    obj = get_object_or_404(Almacen, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Almacén eliminado.')
        return redirect('inv-almacenes-lista')
    return render(request, 'inventario/commons/confirm_delete.html', {'obj': obj, 'back_url': 'inv-almacenes-lista'})
