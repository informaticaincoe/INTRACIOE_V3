"""
Reportes del módulo de Inventario.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, F, Value, DecimalField
from django.db.models.functions import TruncDate, Coalesce
from django.shortcuts import render

from INVENTARIO.models import Producto, MovimientoInventario, Categoria, Almacen


def _parse_fechas(request):
    hoy = date.today()
    try:
        desde = date.fromisoformat(request.GET.get('desde', ''))
    except (ValueError, TypeError):
        desde = hoy.replace(day=1)
    try:
        hasta = date.fromisoformat(request.GET.get('hasta', ''))
    except (ValueError, TypeError):
        hasta = hoy
    return desde, hasta


# ─────────────────────────────────────────────
# Hub
# ─────────────────────────────────────────────
@login_required
def reportes_inventario_hub(request):
    total_productos = Producto.objects.count()
    total_stock = Producto.objects.aggregate(t=Coalesce(Sum('stock'), 0))['t']
    bajo_minimo = Producto.objects.filter(stock__lte=F('stock_minimo'), stock_minimo__gt=0).count()
    sin_stock = Producto.objects.filter(stock=0).count()

    valor_inventario = Producto.objects.aggregate(
        valor=Coalesce(Sum(F('stock') * F('precio_compra'), output_field=DecimalField()), Decimal('0'))
    )['valor']

    # Movimientos últimos 7 días
    hoy = date.today()
    hace_7 = hoy - timedelta(days=6)
    movs_7 = (
        MovimientoInventario.objects
        .filter(fecha__date__range=[hace_7, hoy])
        .annotate(dia=TruncDate('fecha'))
        .values('dia')
        .annotate(
            entradas=Coalesce(Sum('cantidad', filter=Q(tipo='Entrada')), 0),
            salidas=Coalesce(Sum('cantidad', filter=Q(tipo='Salida')), 0),
        )
        .order_by('dia')
    )
    chart_labels = [(hace_7 + timedelta(days=i)).strftime('%d/%m') for i in range(7)]
    datos_map = {d['dia']: d for d in movs_7}
    chart_entradas = [datos_map.get(hace_7 + timedelta(days=i), {}).get('entradas', 0) for i in range(7)]
    chart_salidas = [datos_map.get(hace_7 + timedelta(days=i), {}).get('salidas', 0) for i in range(7)]

    # Top 5 productos con más movimiento del mes
    inicio_mes = hoy.replace(day=1)
    top_movimiento = (
        MovimientoInventario.objects
        .filter(fecha__date__range=[inicio_mes, hoy])
        .values('producto__descripcion')
        .annotate(total_movs=Count('id'))
        .order_by('-total_movs')[:5]
    )

    return render(request, 'inventario/reportes_inventario/hub.html', {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'bajo_minimo': bajo_minimo,
        'sin_stock': sin_stock,
        'valor_inventario': valor_inventario,
        'top_movimiento': top_movimiento,
        'chart_labels': chart_labels,
        'chart_entradas': chart_entradas,
        'chart_salidas': chart_salidas,
    })


# ─────────────────────────────────────────────
# 1. Kardex por producto
# ─────────────────────────────────────────────
@login_required
def reporte_kardex(request):
    desde, hasta = _parse_fechas(request)
    producto_id = request.GET.get('producto', '')

    productos = Producto.objects.all().order_by('descripcion')
    movimientos = []
    producto_sel = None

    if producto_id:
        try:
            producto_sel = Producto.objects.get(pk=producto_id)
            movimientos = (
                MovimientoInventario.objects
                .filter(producto=producto_sel, fecha__date__range=[desde, hasta])
                .select_related('almacen')
                .order_by('fecha')
            )
        except Producto.DoesNotExist:
            pass

    # Calcular saldo acumulado
    saldo = producto_sel.stock if producto_sel else 0
    # Recalcular desde los movimientos en el rango
    movs_list = []
    running = 0
    for m in movimientos:
        if m.tipo == 'Entrada':
            running += m.cantidad
        elif m.tipo == 'Salida':
            running -= m.cantidad
        movs_list.append({'mov': m, 'saldo': running})

    return render(request, 'inventario/reportes_inventario/kardex.html', {
        'productos': productos,
        'producto_sel': producto_sel,
        'movimientos': movs_list,
        'desde': desde, 'hasta': hasta,
        'producto_id': producto_id,
    })


# ─────────────────────────────────────────────
# 2. Inventario valorizado
# ─────────────────────────────────────────────
@login_required
def reporte_inventario_valorizado(request):
    categoria_id = request.GET.get('categoria', '')

    qs = Producto.objects.select_related('categoria', 'unidad_medida').order_by('categoria__nombre', 'descripcion')
    if categoria_id:
        qs = qs.filter(categoria_id=categoria_id)

    productos = []
    for p in qs:
        valor_costo = p.stock * p.precio_compra
        valor_venta = p.stock * p.precio_venta
        productos.append({
            'obj': p,
            'valor_costo': valor_costo,
            'valor_venta': valor_venta,
        })

    resumen = qs.aggregate(
        total_productos=Count('id'),
        total_unidades=Coalesce(Sum('stock'), 0),
        valor_costo=Coalesce(Sum(F('stock') * F('precio_compra'), output_field=DecimalField()), Decimal('0')),
        valor_venta=Coalesce(Sum(F('stock') * F('precio_venta'), output_field=DecimalField()), Decimal('0')),
    )

    categorias = Categoria.objects.all().order_by('nombre')

    return render(request, 'inventario/reportes_inventario/valorizado.html', {
        'productos': productos, 'resumen': resumen,
        'categorias': categorias, 'categoria_id': categoria_id,
    })


# ─────────────────────────────────────────────
# 3. Productos bajo stock mínimo
# ─────────────────────────────────────────────
@login_required
def reporte_bajo_stock(request):
    productos = (
        Producto.objects
        .filter(stock_minimo__gt=0)
        .filter(Q(stock__lte=F('stock_minimo')) | Q(stock=0))
        .select_related('categoria', 'unidad_medida')
        .order_by('stock')
    )

    resumen = {
        'total': productos.count(),
        'sin_stock': productos.filter(stock=0).count(),
        'bajo_minimo': productos.filter(stock__gt=0).count(),
    }

    return render(request, 'inventario/reportes_inventario/bajo_stock.html', {
        'productos': productos, 'resumen': resumen,
    })


# ─────────────────────────────────────────────
# 4. Productos sin movimiento
# ─────────────────────────────────────────────
@login_required
def reporte_sin_movimiento(request):
    dias = int(request.GET.get('dias', 30))
    fecha_limite = date.today() - timedelta(days=dias)

    # Productos con movimiento reciente
    con_movimiento = (
        MovimientoInventario.objects
        .filter(fecha__date__gte=fecha_limite)
        .values_list('producto_id', flat=True)
        .distinct()
    )

    productos = (
        Producto.objects
        .exclude(id__in=con_movimiento)
        .filter(stock__gt=0)
        .select_related('categoria', 'unidad_medida')
        .order_by('-stock')
    )

    valor_muerto = productos.aggregate(
        total=Coalesce(Sum(F('stock') * F('precio_compra'), output_field=DecimalField()), Decimal('0')),
        unidades=Coalesce(Sum('stock'), 0),
    )

    return render(request, 'inventario/reportes_inventario/sin_movimiento.html', {
        'productos': productos, 'valor_muerto': valor_muerto,
        'dias': dias,
    })


# ─────────────────────────────────────────────
# 5. Movimientos por período
# ─────────────────────────────────────────────
@login_required
def reporte_movimientos_periodo(request):
    desde, hasta = _parse_fechas(request)
    tipo_filtro = request.GET.get('tipo', '')

    qs = MovimientoInventario.objects.filter(fecha__date__range=[desde, hasta]).select_related('producto', 'almacen')
    if tipo_filtro:
        qs = qs.filter(tipo=tipo_filtro)

    resumen = qs.aggregate(
        total_movs=Count('id'),
        total_entradas=Coalesce(Sum('cantidad', filter=Q(tipo='Entrada')), 0),
        total_salidas=Coalesce(Sum('cantidad', filter=Q(tipo='Salida')), 0),
        total_ajustes=Coalesce(Sum('cantidad', filter=Q(tipo='Ajuste')), 0),
    )

    # Gráfica por día
    por_dia = (
        qs.annotate(dia=TruncDate('fecha'))
        .values('dia')
        .annotate(
            entradas=Coalesce(Sum('cantidad', filter=Q(tipo='Entrada')), 0),
            salidas=Coalesce(Sum('cantidad', filter=Q(tipo='Salida')), 0),
        )
        .order_by('dia')
    )

    chart_labels = [d['dia'].strftime('%d/%m') for d in por_dia]
    chart_entradas = [d['entradas'] for d in por_dia]
    chart_salidas = [d['salidas'] for d in por_dia]

    return render(request, 'inventario/reportes_inventario/movimientos_periodo.html', {
        'movimientos': qs.order_by('-fecha')[:200],
        'resumen': resumen,
        'desde': desde, 'hasta': hasta, 'tipo_filtro': tipo_filtro,
        'chart_labels': chart_labels,
        'chart_entradas': chart_entradas,
        'chart_salidas': chart_salidas,
    })
