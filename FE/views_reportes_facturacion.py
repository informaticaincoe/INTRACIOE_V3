"""
Reportes del módulo de Facturación.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate, TruncMonth, Coalesce
from django.shortcuts import render

from FE.models import (
    FacturaElectronica, DetalleFactura,
    EventoInvalidacion, Tipo_dte,
)


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


def _base_qs():
    return FacturaElectronica.objects.select_related('dtereceptor', 'tipo_dte')


# ─────────────────────────────────────────────
# Hub
# ─────────────────────────────────────────────
@login_required
def reportes_facturacion_hub(request):
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    mes_prev_fin = inicio_mes - timedelta(days=1)
    mes_prev_ini = mes_prev_fin.replace(day=1)

    qs = _base_qs().exclude(dte_invalidacion__recibido_mh=True)

    mes_actual = qs.filter(fecha_emision__range=[inicio_mes, hoy]).aggregate(
        docs=Count('id'),
        total=Coalesce(Sum('total_pagar'), Decimal('0')),
        iva=Coalesce(Sum('total_iva'), Decimal('0')),
    )

    mes_prev = qs.filter(fecha_emision__range=[mes_prev_ini, mes_prev_fin]).aggregate(
        total=Coalesce(Sum('total_pagar'), Decimal('0')),
    )

    variacion = None
    if mes_prev['total'] and mes_prev['total'] > 0:
        variacion = ((mes_actual['total'] - mes_prev['total']) / mes_prev['total'] * 100)

    # Por tipo de documento este mes
    por_tipo = (
        qs.filter(fecha_emision__range=[inicio_mes, hoy])
        .values('tipo_dte__descripcion')
        .annotate(cantidad=Count('id'), total=Coalesce(Sum('total_pagar'), Decimal('0')))
        .order_by('-total')
    )

    # Anulaciones del mes
    anulaciones_mes = EventoInvalidacion.objects.filter(
        fecha_anulacion__range=[inicio_mes, hoy]
    ).count()

    # Últimos 7 días
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

    tipo_labels = [t['tipo_dte__descripcion'] for t in por_tipo]
    tipo_valores = [float(t['total']) for t in por_tipo]

    return render(request, 'facturacion/reportes/hub.html', {
        'mes_actual': mes_actual, 'mes_prev': mes_prev, 'variacion': variacion,
        'por_tipo': por_tipo, 'anulaciones_mes': anulaciones_mes,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
        'tipo_labels': tipo_labels, 'tipo_valores': tipo_valores,
    })


# ─────────────────────────────────────────────
# 1. Libro de ventas contribuyente (CCF)
# ─────────────────────────────────────────────
@login_required
def reporte_libro_contribuyente(request):
    desde, hasta = _parse_fechas(request)

    facturas = (
        _base_qs()
        .filter(fecha_emision__range=[desde, hasta], tipo_dte__codigo='03')
        .exclude(dte_invalidacion__recibido_mh=True)
        .order_by('fecha_emision', 'numero_control')
    )

    resumen = facturas.aggregate(
        total_docs=Count('id'),
        total_gravadas=Coalesce(Sum('total_gravadas'), Decimal('0')),
        total_exentas=Coalesce(Sum('total_exentas'), Decimal('0')),
        total_iva=Coalesce(Sum('total_iva'), Decimal('0')),
        total_retenido=Coalesce(Sum('iva_retenido'), Decimal('0')),
        total_pagar=Coalesce(Sum('total_pagar'), Decimal('0')),
    )

    return render(request, 'facturacion/reportes/libro_contribuyente.html', {
        'facturas': facturas, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
    })


# ─────────────────────────────────────────────
# 2. Libro de ventas consumidor final
# ─────────────────────────────────────────────
@login_required
def reporte_libro_consumidor(request):
    desde, hasta = _parse_fechas(request)

    facturas = (
        _base_qs()
        .filter(fecha_emision__range=[desde, hasta], tipo_dte__codigo='01')
        .exclude(dte_invalidacion__recibido_mh=True)
        .order_by('fecha_emision', 'numero_control')
    )

    resumen = facturas.aggregate(
        total_docs=Count('id'),
        total_gravadas=Coalesce(Sum('total_gravadas'), Decimal('0')),
        total_exentas=Coalesce(Sum('total_exentas'), Decimal('0')),
        total_iva=Coalesce(Sum('total_iva'), Decimal('0')),
        total_pagar=Coalesce(Sum('total_pagar'), Decimal('0')),
    )

    return render(request, 'facturacion/reportes/libro_consumidor.html', {
        'facturas': facturas, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
    })


# ─────────────────────────────────────────────
# 3. Resumen de DTE por tipo
# ─────────────────────────────────────────────
@login_required
def reporte_resumen_dte(request):
    desde, hasta = _parse_fechas(request)

    qs = _base_qs().filter(fecha_emision__range=[desde, hasta])

    por_tipo = (
        qs.values('tipo_dte__codigo', 'tipo_dte__descripcion')
        .annotate(
            cantidad=Count('id'),
            total=Coalesce(Sum('total_pagar'), Decimal('0')),
            iva=Coalesce(Sum('total_iva'), Decimal('0')),
            anuladas=Count('id', filter=Q(dte_invalidacion__recibido_mh=True)),
        )
        .order_by('tipo_dte__codigo')
    )

    resumen = qs.aggregate(
        total_docs=Count('id'),
        total_monto=Coalesce(Sum('total_pagar'), Decimal('0')),
    )

    chart_labels = [t['tipo_dte__descripcion'] for t in por_tipo]
    chart_valores = [float(t['total']) for t in por_tipo]

    return render(request, 'facturacion/reportes/resumen_dte.html', {
        'por_tipo': por_tipo, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 4. Documentos anulados
# ─────────────────────────────────────────────
@login_required
def reporte_documentos_anulados(request):
    desde, hasta = _parse_fechas(request)

    anulaciones = (
        EventoInvalidacion.objects
        .filter(fecha_anulacion__range=[desde, hasta])
        .select_related('factura', 'factura__tipo_dte', 'factura__dtereceptor', 'tipo_invalidacion')
        .order_by('-fecha_anulacion')
    )

    resumen = anulaciones.aggregate(
        total_anulaciones=Count('id'),
        total_monto=Coalesce(
            Sum('factura__total_pagar'),
            Decimal('0'),
        ),
    )

    return render(request, 'facturacion/reportes/documentos_anulados.html', {
        'anulaciones': anulaciones, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
    })


# ─────────────────────────────────────────────
# 5. Reporte de retenciones
# ─────────────────────────────────────────────
@login_required
def reporte_retenciones(request):
    desde, hasta = _parse_fechas(request)

    facturas = (
        _base_qs()
        .filter(
            fecha_emision__range=[desde, hasta],
        )
        .filter(Q(iva_retenido__gt=0) | Q(retencion_renta__gt=0))
        .exclude(dte_invalidacion__recibido_mh=True)
        .order_by('fecha_emision')
    )

    resumen = facturas.aggregate(
        total_docs=Count('id'),
        total_iva_retenido=Coalesce(Sum('iva_retenido'), Decimal('0')),
        total_renta_retenida=Coalesce(Sum('retencion_renta'), Decimal('0')),
        total_facturado=Coalesce(Sum('total_pagar'), Decimal('0')),
    )

    return render(request, 'facturacion/reportes/retenciones.html', {
        'facturas': facturas, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
    })
