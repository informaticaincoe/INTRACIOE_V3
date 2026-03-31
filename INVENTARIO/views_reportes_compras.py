"""
Reportes del módulo de Compras.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate, TruncMonth, Coalesce
from django.shortcuts import render

from INVENTARIO.models import Compra, DetalleCompra, Proveedor


def _parse_fechas(request):
    hoy = date.today()
    desde_str = request.GET.get('desde', '')
    hasta_str = request.GET.get('hasta', '')
    try:
        desde = date.fromisoformat(desde_str)
    except (ValueError, TypeError):
        desde = hoy.replace(day=1)
    try:
        hasta = date.fromisoformat(hasta_str)
    except (ValueError, TypeError):
        hasta = hoy
    return desde, hasta


def _base_compras_qs():
    return Compra.objects.exclude(estado='Cancelado')


# ─────────────────────────────────────────────
# Hub de reportes
# ─────────────────────────────────────────────
@login_required
def reportes_compras_hub(request):
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    mes_anterior_fin = inicio_mes - timedelta(days=1)
    mes_anterior_ini = mes_anterior_fin.replace(day=1)

    qs = _base_compras_qs()

    mes_actual = qs.filter(fecha__date__range=[inicio_mes, hoy]).aggregate(
        compras=Count('id'),
        total=Coalesce(Sum('total'), Decimal('0')),
        proveedores=Count('proveedor', distinct=True),
    )

    mes_prev = qs.filter(fecha__date__range=[mes_anterior_ini, mes_anterior_fin]).aggregate(
        total=Coalesce(Sum('total'), Decimal('0')),
    )

    if mes_prev['total'] and mes_prev['total'] > 0:
        variacion = ((mes_actual['total'] - mes_prev['total']) / mes_prev['total'] * 100)
    else:
        variacion = None

    compras_hoy = qs.filter(fecha__date=hoy).aggregate(
        compras=Count('id'),
        total=Coalesce(Sum('total'), Decimal('0')),
    )

    top_productos = (
        DetalleCompra.objects
        .filter(compra__fecha__date__range=[inicio_mes, hoy])
        .exclude(compra__estado='Cancelado')
        .values('producto__descripcion')
        .annotate(cantidad=Coalesce(Sum('cantidad'), 0))
        .order_by('-cantidad')[:5]
    )

    top_proveedores = (
        qs.filter(fecha__date__range=[inicio_mes, hoy])
        .values('proveedor__nombre')
        .annotate(total=Coalesce(Sum('total'), Decimal('0')))
        .order_by('-total')[:5]
    )

    # Últimos 7 días
    hace_7 = hoy - timedelta(days=6)
    ultimos_7 = (
        qs.filter(fecha__date__range=[hace_7, hoy])
        .annotate(dia=TruncDate('fecha'))
        .values('dia')
        .annotate(total=Coalesce(Sum('total'), Decimal('0')))
        .order_by('dia')
    )
    chart_labels = [(hace_7 + timedelta(days=i)).strftime('%d/%m') for i in range(7)]
    datos_map = {d['dia']: float(d['total']) for d in ultimos_7}
    chart_valores = [datos_map.get(hace_7 + timedelta(days=i), 0) for i in range(7)]

    return render(request, 'inventario/reportes_compras/hub.html', {
        'mes_actual': mes_actual,
        'mes_prev': mes_prev,
        'variacion': variacion,
        'compras_hoy': compras_hoy,
        'top_productos': top_productos,
        'top_proveedores': top_proveedores,
        'chart_labels': chart_labels,
        'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 1. Compras por período
# ─────────────────────────────────────────────
@login_required
def reporte_compras_periodo(request):
    desde, hasta = _parse_fechas(request)
    agrupacion = request.GET.get('agrupar', 'dia')

    qs = _base_compras_qs().filter(fecha__date__range=[desde, hasta])

    trunc = TruncMonth('fecha') if agrupacion == 'mes' else TruncDate('fecha')
    datos = (
        qs.annotate(periodo=trunc)
        .values('periodo')
        .annotate(
            cantidad=Count('id'),
            total=Coalesce(Sum('total'), Decimal('0')),
        )
        .order_by('periodo')
    )

    resumen = qs.aggregate(
        total_compras=Count('id'),
        total_monto=Coalesce(Sum('total'), Decimal('0')),
    )

    fmt = '%b %Y' if agrupacion == 'mes' else '%d/%m'
    labels = [d['periodo'].strftime(fmt) if d['periodo'] else '' for d in datos]
    valores = [float(d['total']) for d in datos]

    return render(request, 'inventario/reportes_compras/compras_periodo.html', {
        'datos': datos, 'resumen': resumen,
        'desde': desde, 'hasta': hasta, 'agrupacion': agrupacion,
        'chart_labels': labels, 'chart_valores': valores,
    })


# ─────────────────────────────────────────────
# 2. Compras por proveedor
# ─────────────────────────────────────────────
@login_required
def reporte_compras_proveedor(request):
    desde, hasta = _parse_fechas(request)
    limit = int(request.GET.get('limit', 20))

    proveedores = (
        _base_compras_qs()
        .filter(fecha__date__range=[desde, hasta])
        .values('proveedor__id', 'proveedor__nombre', 'proveedor__num_documento')
        .annotate(
            total_compras=Count('id'),
            total_monto=Coalesce(Sum('total'), Decimal('0')),
        )
        .order_by('-total_monto')[:limit]
    )

    resumen = _base_compras_qs().filter(fecha__date__range=[desde, hasta]).aggregate(
        total_general=Coalesce(Sum('total'), Decimal('0')),
        total_proveedores=Count('proveedor', distinct=True),
    )

    chart_labels = [p['proveedor__nombre'][:25] for p in proveedores]
    chart_valores = [float(p['total_monto']) for p in proveedores]

    return render(request, 'inventario/reportes_compras/compras_proveedor.html', {
        'proveedores': proveedores, 'resumen': resumen,
        'desde': desde, 'hasta': hasta, 'limit': limit,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 3. Productos más comprados
# ─────────────────────────────────────────────
@login_required
def reporte_productos_comprados(request):
    desde, hasta = _parse_fechas(request)
    limit = int(request.GET.get('limit', 20))

    productos = (
        DetalleCompra.objects
        .filter(compra__fecha__date__range=[desde, hasta])
        .exclude(compra__estado='Cancelado')
        .values('producto__codigo', 'producto__descripcion', 'producto__categoria__nombre')
        .annotate(
            cantidad_comprada=Coalesce(Sum('cantidad'), 0),
            total_monto=Coalesce(Sum('subtotal'), Decimal('0')),
        )
        .order_by('-cantidad_comprada')[:limit]
    )

    resumen = (
        DetalleCompra.objects
        .filter(compra__fecha__date__range=[desde, hasta])
        .exclude(compra__estado='Cancelado')
        .aggregate(
            total_items=Coalesce(Sum('cantidad'), 0),
            total_monto=Coalesce(Sum('subtotal'), Decimal('0')),
            total_productos=Count('producto', distinct=True),
        )
    )

    chart_labels = [p['producto__descripcion'][:25] for p in productos]
    chart_valores = [int(p['cantidad_comprada']) for p in productos]

    return render(request, 'inventario/reportes_compras/productos_comprados.html', {
        'productos': productos, 'resumen': resumen,
        'desde': desde, 'hasta': hasta, 'limit': limit,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 4. Cuentas por pagar
# ─────────────────────────────────────────────
@login_required
def reporte_cuentas_por_pagar(request):
    from CONTABILIDAD.models import CuentaPorPagar

    estado_filtro = request.GET.get('estado', '')

    qs = CuentaPorPagar.objects.select_related('proveedor', 'compra').order_by('fecha_vencimiento')
    if estado_filtro:
        qs = qs.filter(estado=estado_filtro)
    else:
        qs = qs.exclude(estado__in=['PAGADO', 'ANULADO'])

    resumen = qs.aggregate(
        total_pendiente=Coalesce(Sum('monto_original'), Decimal('0')),
        total_cuentas=Count('id'),
    )

    # Antigüedad de saldos
    hoy = date.today()
    por_vencer = qs.filter(fecha_vencimiento__gt=hoy).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))
    vencido_30 = qs.filter(fecha_vencimiento__range=[hoy - timedelta(days=30), hoy]).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))
    vencido_60 = qs.filter(fecha_vencimiento__range=[hoy - timedelta(days=60), hoy - timedelta(days=31)]).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))
    vencido_90 = qs.filter(fecha_vencimiento__lt=hoy - timedelta(days=60)).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))

    antiguedad = [
        {'rango': 'Por vencer', 'monto': por_vencer['t'], 'color': '#16a34a'},
        {'rango': '1-30 días', 'monto': vencido_30['t'], 'color': '#ca8a04'},
        {'rango': '31-60 días', 'monto': vencido_60['t'], 'color': '#ea580c'},
        {'rango': '+60 días', 'monto': vencido_90['t'], 'color': '#dc2626'},
    ]

    chart_labels = [a['rango'] for a in antiguedad]
    chart_valores = [float(a['monto']) for a in antiguedad]
    chart_colores = [a['color'] for a in antiguedad]

    return render(request, 'inventario/reportes_compras/cuentas_por_pagar.html', {
        'cuentas': qs, 'resumen': resumen,
        'antiguedad': antiguedad, 'estado_filtro': estado_filtro,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
        'chart_colores': chart_colores,
    })


# ─────────────────────────────────────────────
# 5. Comparativo de compras
# ─────────────────────────────────────────────
@login_required
def reporte_comparativo_compras(request):
    hoy = date.today()
    meses = int(request.GET.get('meses', 6))

    datos = []
    for i in range(meses - 1, -1, -1):
        primer_dia = (hoy.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        if i == 0:
            ultimo_dia = hoy
        else:
            siguiente = (primer_dia + timedelta(days=32)).replace(day=1)
            ultimo_dia = siguiente - timedelta(days=1)

        agg = _base_compras_qs().filter(
            fecha__date__range=[primer_dia, ultimo_dia]
        ).aggregate(
            compras=Count('id'),
            total=Coalesce(Sum('total'), Decimal('0')),
        )
        datos.append({
            'periodo': primer_dia,
            'label': primer_dia.strftime('%b %Y'),
            'compras': agg['compras'],
            'total': agg['total'],
        })

    # Variación mes a mes
    for i in range(1, len(datos)):
        prev = datos[i - 1]['total']
        curr = datos[i]['total']
        if prev and prev > 0:
            datos[i]['variacion'] = ((curr - prev) / prev * 100)
        else:
            datos[i]['variacion'] = None

    if datos:
        datos[0]['variacion'] = None

    chart_labels = [d['label'] for d in datos]
    chart_valores = [float(d['total']) for d in datos]

    return render(request, 'inventario/reportes_compras/comparativo.html', {
        'datos': datos, 'meses': meses,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
    })
