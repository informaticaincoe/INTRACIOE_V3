"""
Reportes del módulo de Ventas.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, Q, Value, DecimalField
from django.db.models.functions import TruncDate, TruncMonth, Coalesce
from django.shortcuts import render
from django.utils import timezone

from FE.models import FacturaElectronica, DetalleFactura, Receptor_fe


# ─────────────────────────────────────────────
# Hub de reportes (cuadritos)
# ─────────────────────────────────────────────
@login_required
def reportes_ventas_hub(request):
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    mes_anterior_fin = inicio_mes - timedelta(days=1)
    mes_anterior_ini = mes_anterior_fin.replace(day=1)

    qs = _base_ventas_qs()

    # Mes actual
    mes_actual = qs.filter(fecha_emision__range=[inicio_mes, hoy]).aggregate(
        facturas=Count('id'),
        total=Coalesce(Sum('total_pagar'), Decimal('0')),
        iva=Coalesce(Sum('total_iva'), Decimal('0')),
        clientes=Count('dtereceptor', distinct=True),
    )

    # Mes anterior
    mes_prev = qs.filter(fecha_emision__range=[mes_anterior_ini, mes_anterior_fin]).aggregate(
        facturas=Count('id'),
        total=Coalesce(Sum('total_pagar'), Decimal('0')),
    )

    # Variación porcentual
    if mes_prev['total'] and mes_prev['total'] > 0:
        variacion = ((mes_actual['total'] - mes_prev['total']) / mes_prev['total'] * 100)
    else:
        variacion = None

    # Hoy
    ventas_hoy = qs.filter(fecha_emision=hoy).aggregate(
        facturas=Count('id'),
        total=Coalesce(Sum('total_pagar'), Decimal('0')),
    )

    # Top 5 productos del mes
    top_productos = (
        DetalleFactura.objects
        .filter(factura__fecha_emision__range=[inicio_mes, hoy])
        .exclude(factura__dte_invalidacion__recibido_mh=True)
        .values('producto__descripcion')
        .annotate(cantidad=Coalesce(Sum('cantidad'), 0))
        .order_by('-cantidad')[:5]
    )

    # Top 5 clientes del mes
    top_clientes = (
        qs.filter(fecha_emision__range=[inicio_mes, hoy])
        .values('dtereceptor__nombre')
        .annotate(total=Coalesce(Sum('total_pagar'), Decimal('0')))
        .order_by('-total')[:5]
    )

    # Ventas últimos 7 días para mini gráfica
    hace_7 = hoy - timedelta(days=6)
    ultimos_7 = (
        qs.filter(fecha_emision__range=[hace_7, hoy])
        .annotate(dia=TruncDate('fecha_emision'))
        .values('dia')
        .annotate(total=Coalesce(Sum('total_pagar'), Decimal('0')))
        .order_by('dia')
    )
    chart_labels = [(hace_7 + timedelta(days=i)).strftime('%d/%m') for i in range(7)]
    datos_map = {d['dia']: float(d['total']) for d in ultimos_7}
    chart_valores = [datos_map.get(hace_7 + timedelta(days=i), 0) for i in range(7)]

    return render(request, 'ventas/reportes/hub.html', {
        'mes_actual': mes_actual,
        'mes_prev': mes_prev,
        'variacion': variacion,
        'ventas_hoy': ventas_hoy,
        'top_productos': top_productos,
        'top_clientes': top_clientes,
        'chart_labels': chart_labels,
        'chart_valores': chart_valores,
        'hoy': hoy,
        'inicio_mes': inicio_mes,
    })


def _base_ventas_qs():
    """QuerySet base: facturas no anuladas."""
    return FacturaElectronica.objects.exclude(
        dte_invalidacion__recibido_mh=True
    )


def _parse_fechas(request):
    """Extrae fecha_desde y fecha_hasta del GET, con defaults sensatos."""
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


# ─────────────────────────────────────────────
# 1. Ventas por período
# ─────────────────────────────────────────────
@login_required
def reporte_ventas_periodo(request):
    desde, hasta = _parse_fechas(request)
    agrupacion = request.GET.get('agrupar', 'dia')  # dia | mes

    qs = _base_ventas_qs().filter(fecha_emision__range=[desde, hasta])

    if agrupacion == 'mes':
        datos = (
            qs.annotate(periodo=TruncMonth('fecha_emision'))
            .values('periodo')
            .annotate(
                cantidad=Count('id'),
                total=Coalesce(Sum('total_pagar'), Decimal('0')),
                iva=Coalesce(Sum('total_iva'), Decimal('0')),
            )
            .order_by('periodo')
        )
    else:
        datos = (
            qs.annotate(periodo=TruncDate('fecha_emision'))
            .values('periodo')
            .annotate(
                cantidad=Count('id'),
                total=Coalesce(Sum('total_pagar'), Decimal('0')),
                iva=Coalesce(Sum('total_iva'), Decimal('0')),
            )
            .order_by('periodo')
        )

    resumen = qs.aggregate(
        total_facturas=Count('id'),
        total_monto=Coalesce(Sum('total_pagar'), Decimal('0')),
        total_iva=Coalesce(Sum('total_iva'), Decimal('0')),
    )

    # Datos para gráfica
    labels = []
    valores = []
    for d in datos:
        if agrupacion == 'mes':
            labels.append(d['periodo'].strftime('%b %Y') if d['periodo'] else '')
        else:
            labels.append(d['periodo'].strftime('%d/%m') if d['periodo'] else '')
        valores.append(float(d['total']))

    return render(request, 'ventas/reportes/ventas_periodo.html', {
        'datos': datos,
        'resumen': resumen,
        'desde': desde,
        'hasta': hasta,
        'agrupacion': agrupacion,
        'chart_labels': labels,
        'chart_valores': valores,
    })


# ─────────────────────────────────────────────
# 2. Top clientes
# ─────────────────────────────────────────────
@login_required
def reporte_top_clientes(request):
    desde, hasta = _parse_fechas(request)
    limit = int(request.GET.get('limit', 20))

    clientes = (
        _base_ventas_qs()
        .filter(fecha_emision__range=[desde, hasta])
        .values(
            'dtereceptor__id',
            'dtereceptor__nombre',
            'dtereceptor__num_documento',
        )
        .annotate(
            total_compras=Count('id'),
            total_monto=Coalesce(Sum('total_pagar'), Decimal('0')),
            total_iva=Coalesce(Sum('total_iva'), Decimal('0')),
        )
        .order_by('-total_monto')[:limit]
    )

    resumen = _base_ventas_qs().filter(
        fecha_emision__range=[desde, hasta]
    ).aggregate(
        total_general=Coalesce(Sum('total_pagar'), Decimal('0')),
        total_clientes=Count('dtereceptor', distinct=True),
    )

    # Datos para gráfica
    chart_labels = [c['dtereceptor__nombre'][:25] for c in clientes]
    chart_valores = [float(c['total_monto']) for c in clientes]

    return render(request, 'ventas/reportes/top_clientes.html', {
        'clientes': clientes,
        'resumen': resumen,
        'desde': desde,
        'hasta': hasta,
        'limit': limit,
        'chart_labels': chart_labels,
        'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 3. Productos más vendidos
# ─────────────────────────────────────────────
@login_required
def reporte_productos_vendidos(request):
    desde, hasta = _parse_fechas(request)
    limit = int(request.GET.get('limit', 20))

    productos = (
        DetalleFactura.objects
        .filter(
            factura__fecha_emision__range=[desde, hasta],
        )
        .exclude(factura__dte_invalidacion__recibido_mh=True)
        .values(
            'producto__codigo',
            'producto__descripcion',
            'producto__categoria__nombre',
        )
        .annotate(
            cantidad_vendida=Coalesce(Sum('cantidad'), 0),
            total_monto=Coalesce(Sum('ventas_gravadas'), Decimal('0')),
        )
        .order_by('-cantidad_vendida')[:limit]
    )

    resumen = (
        DetalleFactura.objects
        .filter(factura__fecha_emision__range=[desde, hasta])
        .exclude(factura__dte_invalidacion__recibido_mh=True)
        .aggregate(
            total_items=Coalesce(Sum('cantidad'), 0),
            total_monto=Coalesce(Sum('ventas_gravadas'), Decimal('0')),
            total_productos=Count('producto', distinct=True),
        )
    )

    chart_labels = [p['producto__descripcion'][:25] for p in productos]
    chart_valores = [int(p['cantidad_vendida']) for p in productos]

    return render(request, 'ventas/reportes/productos_vendidos.html', {
        'productos': productos,
        'resumen': resumen,
        'desde': desde,
        'hasta': hasta,
        'limit': limit,
        'chart_labels': chart_labels,
        'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 4. Ventas por vendedor
# ─────────────────────────────────────────────
@login_required
def reporte_ventas_vendedor(request):
    desde, hasta = _parse_fechas(request)

    # Agrupa por el usuario que generó la factura (si existe campo)
    # Usamos el campo dteemisor como proxy — en sistemas multi-usuario
    # se puede agregar un campo "vendedor" al modelo. Por ahora agrupamos
    # por el usuario que creó la factura si existe, o mostramos todas.
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Si FacturaElectronica no tiene campo vendedor, agrupamos por tipo_dte
    # como reporte de ventas por tipo de documento
    vendedores = (
        _base_ventas_qs()
        .filter(fecha_emision__range=[desde, hasta])
        .values(
            'tipo_dte__descripcion',
            'tipo_dte__codigo',
        )
        .annotate(
            cantidad=Count('id'),
            total_monto=Coalesce(Sum('total_pagar'), Decimal('0')),
            total_iva=Coalesce(Sum('total_iva'), Decimal('0')),
        )
        .order_by('-total_monto')
    )

    resumen = _base_ventas_qs().filter(
        fecha_emision__range=[desde, hasta]
    ).aggregate(
        total_facturas=Count('id'),
        total_monto=Coalesce(Sum('total_pagar'), Decimal('0')),
    )

    chart_labels = [v['tipo_dte__descripcion'] for v in vendedores]
    chart_valores = [float(v['total_monto']) for v in vendedores]

    return render(request, 'ventas/reportes/ventas_vendedor.html', {
        'vendedores': vendedores,
        'resumen': resumen,
        'desde': desde,
        'hasta': hasta,
        'chart_labels': chart_labels,
        'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 5. Devoluciones
# ─────────────────────────────────────────────
@login_required
def reporte_devoluciones(request):
    desde, hasta = _parse_fechas(request)

    # Las notas de crédito (tipo_dte código '05') son devoluciones
    devoluciones = (
        FacturaElectronica.objects
        .filter(
            fecha_emision__range=[desde, hasta],
            tipo_dte__codigo='05',
        )
        .select_related('dtereceptor', 'tipo_dte')
        .order_by('-fecha_emision')
    )

    resumen = devoluciones.aggregate(
        total_devoluciones=Count('id'),
        total_monto=Coalesce(Sum('total_pagar'), Decimal('0')),
    )

    return render(request, 'ventas/reportes/devoluciones.html', {
        'devoluciones': devoluciones,
        'resumen': resumen,
        'desde': desde,
        'hasta': hasta,
    })
