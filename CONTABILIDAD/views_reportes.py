"""
Reportes del módulo de Contabilidad.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import Coalesce
from django.shortcuts import render

from CONTABILIDAD.models import (
    AsientoContable, LineaAsiento, CuentaContable,
    CuentaPorCobrar, CuentaPorPagar,
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


# ─────────────────────────────────────────────
# Hub
# ─────────────────────────────────────────────
@login_required
def reportes_contabilidad_hub(request):
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)

    asientos_mes = AsientoContable.objects.filter(fecha__range=[inicio_mes, hoy])
    total_asientos = asientos_mes.count()
    confirmados = asientos_mes.filter(estado='CONFIRMADO').count()
    borradores = asientos_mes.filter(estado='BORRADOR').count()

    total_debe = LineaAsiento.objects.filter(
        asiento__fecha__range=[inicio_mes, hoy], asiento__estado='CONFIRMADO'
    ).aggregate(t=Coalesce(Sum('debe'), Decimal('0')))['t']

    cxc_pendiente = CuentaPorCobrar.objects.exclude(
        estado__in=['PAGADO', 'ANULADO']
    ).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))['t']

    cxp_pendiente = CuentaPorPagar.objects.exclude(
        estado__in=['PAGADO', 'ANULADO']
    ).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))['t']

    cxc_vencidas = CuentaPorCobrar.objects.filter(
        fecha_vencimiento__lt=hoy
    ).exclude(estado__in=['PAGADO', 'ANULADO']).count()

    cxp_vencidas = CuentaPorPagar.objects.filter(
        fecha_vencimiento__lt=hoy
    ).exclude(estado__in=['PAGADO', 'ANULADO']).count()

    return render(request, 'contabilidad/reportes/hub.html', {
        'total_asientos': total_asientos, 'confirmados': confirmados,
        'borradores': borradores, 'total_debe': total_debe,
        'cxc_pendiente': cxc_pendiente, 'cxp_pendiente': cxp_pendiente,
        'cxc_vencidas': cxc_vencidas, 'cxp_vencidas': cxp_vencidas,
    })


# ─────────────────────────────────────────────
# 1. Flujo de efectivo
# ─────────────────────────────────────────────
@login_required
def reporte_flujo_efectivo(request):
    desde, hasta = _parse_fechas(request)

    lineas = LineaAsiento.objects.filter(
        asiento__fecha__range=[desde, hasta],
        asiento__estado='CONFIRMADO',
    ).select_related('cuenta', 'asiento')

    ingresos = lineas.filter(cuenta__tipo='INGRESO').aggregate(
        total=Coalesce(Sum('haber') - Sum('debe'), Decimal('0'))
    )['total']
    gastos = lineas.filter(cuenta__tipo='GASTO').aggregate(
        total=Coalesce(Sum('debe') - Sum('haber'), Decimal('0'))
    )['total']
    flujo_neto = ingresos - gastos

    # Por tipo de cuenta
    por_tipo = (
        lineas.values('cuenta__tipo')
        .annotate(
            total_debe=Coalesce(Sum('debe'), Decimal('0')),
            total_haber=Coalesce(Sum('haber'), Decimal('0')),
        )
        .order_by('cuenta__tipo')
    )

    return render(request, 'contabilidad/reportes/flujo_efectivo.html', {
        'ingresos': ingresos, 'gastos': gastos, 'flujo_neto': flujo_neto,
        'por_tipo': por_tipo, 'desde': desde, 'hasta': hasta,
    })


# ─────────────────────────────────────────────
# 2. Antigüedad saldos CxC
# ─────────────────────────────────────────────
@login_required
def reporte_antiguedad_cxc(request):
    hoy = date.today()
    qs = CuentaPorCobrar.objects.exclude(estado__in=['PAGADO', 'ANULADO']).select_related('receptor', 'factura')

    por_vencer = qs.filter(fecha_vencimiento__gt=hoy).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))
    v30 = qs.filter(fecha_vencimiento__range=[hoy - timedelta(days=30), hoy]).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))
    v60 = qs.filter(fecha_vencimiento__range=[hoy - timedelta(days=60), hoy - timedelta(days=31)]).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))
    v90 = qs.filter(fecha_vencimiento__lt=hoy - timedelta(days=60)).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))

    antiguedad = [
        {'rango': 'Por vencer', 'monto': por_vencer['t'], 'color': '#16a34a'},
        {'rango': '1-30 días', 'monto': v30['t'], 'color': '#ca8a04'},
        {'rango': '31-60 días', 'monto': v60['t'], 'color': '#ea580c'},
        {'rango': '+60 días', 'monto': v90['t'], 'color': '#dc2626'},
    ]

    resumen = qs.aggregate(total=Coalesce(Sum('monto_original'), Decimal('0')), cuentas=Count('id'))
    chart_labels = [a['rango'] for a in antiguedad]
    chart_valores = [float(a['monto']) for a in antiguedad]
    chart_colores = [a['color'] for a in antiguedad]

    return render(request, 'contabilidad/reportes/antiguedad_cxc.html', {
        'cuentas': qs.order_by('fecha_vencimiento'), 'resumen': resumen,
        'antiguedad': antiguedad,
        'chart_labels': chart_labels, 'chart_valores': chart_valores, 'chart_colores': chart_colores,
    })


# ─────────────────────────────────────────────
# 3. Antigüedad saldos CxP
# ─────────────────────────────────────────────
@login_required
def reporte_antiguedad_cxp(request):
    hoy = date.today()
    qs = CuentaPorPagar.objects.exclude(estado__in=['PAGADO', 'ANULADO']).select_related('proveedor', 'compra')

    por_vencer = qs.filter(fecha_vencimiento__gt=hoy).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))
    v30 = qs.filter(fecha_vencimiento__range=[hoy - timedelta(days=30), hoy]).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))
    v60 = qs.filter(fecha_vencimiento__range=[hoy - timedelta(days=60), hoy - timedelta(days=31)]).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))
    v90 = qs.filter(fecha_vencimiento__lt=hoy - timedelta(days=60)).aggregate(t=Coalesce(Sum('monto_original'), Decimal('0')))

    antiguedad = [
        {'rango': 'Por vencer', 'monto': por_vencer['t'], 'color': '#16a34a'},
        {'rango': '1-30 días', 'monto': v30['t'], 'color': '#ca8a04'},
        {'rango': '31-60 días', 'monto': v60['t'], 'color': '#ea580c'},
        {'rango': '+60 días', 'monto': v90['t'], 'color': '#dc2626'},
    ]

    resumen = qs.aggregate(total=Coalesce(Sum('monto_original'), Decimal('0')), cuentas=Count('id'))
    chart_labels = [a['rango'] for a in antiguedad]
    chart_valores = [float(a['monto']) for a in antiguedad]
    chart_colores = [a['color'] for a in antiguedad]

    return render(request, 'contabilidad/reportes/antiguedad_cxp.html', {
        'cuentas': qs.order_by('fecha_vencimiento'), 'resumen': resumen,
        'antiguedad': antiguedad,
        'chart_labels': chart_labels, 'chart_valores': chart_valores, 'chart_colores': chart_colores,
    })


# ─────────────────────────────────────────────
# 4. Retenciones IVA/Renta
# ─────────────────────────────────────────────
@login_required
def reporte_retenciones_cont(request):
    desde, hasta = _parse_fechas(request)
    from FE.models import FacturaElectronica

    facturas = (
        FacturaElectronica.objects
        .filter(fecha_emision__range=[desde, hasta])
        .filter(Q(iva_retenido__gt=0) | Q(retencion_renta__gt=0))
        .exclude(dte_invalidacion__recibido_mh=True)
        .select_related('dtereceptor', 'tipo_dte')
        .order_by('fecha_emision')
    )

    resumen = facturas.aggregate(
        total_iva=Coalesce(Sum('iva_retenido'), Decimal('0')),
        total_renta=Coalesce(Sum('retencion_renta'), Decimal('0')),
        docs=Count('id'),
    )

    return render(request, 'contabilidad/reportes/retenciones.html', {
        'facturas': facturas, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
    })


# ─────────────────────────────────────────────
# 5. Conciliación bancaria (resumen)
# ─────────────────────────────────────────────
@login_required
def reporte_conciliacion(request):
    desde, hasta = _parse_fechas(request)

    # Movimientos contables en cuentas tipo banco (ACTIVO con "banco" o "bank" en nombre)
    lineas_banco = (
        LineaAsiento.objects
        .filter(
            asiento__fecha__range=[desde, hasta],
            asiento__estado='CONFIRMADO',
            cuenta__tipo='ACTIVO',
            cuenta__nombre__icontains='banco',
        )
        .select_related('asiento', 'cuenta')
        .order_by('asiento__fecha')
    )

    resumen = lineas_banco.aggregate(
        total_debe=Coalesce(Sum('debe'), Decimal('0')),
        total_haber=Coalesce(Sum('haber'), Decimal('0')),
        movimientos=Count('id'),
    )
    resumen['saldo'] = resumen['total_debe'] - resumen['total_haber']

    return render(request, 'contabilidad/reportes/conciliacion.html', {
        'lineas': lineas_banco, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
    })
