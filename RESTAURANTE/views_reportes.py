"""
Reportes del módulo de Restaurante.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, Q, F
from django.db.models.functions import TruncDate, Coalesce
from django.shortcuts import render

from RESTAURANTE.models import Pedido, Mesa, Comanda, Caja, MovimientosCaja, Platillo, DetallePedido


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
def reportes_restaurante_hub(request):
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)

    pedidos_mes = Pedido.objects.filter(
        creado_el__date__range=[inicio_mes, hoy]
    ).exclude(estado='ANULADO')

    resumen = pedidos_mes.aggregate(
        total_pedidos=Count('id'),
        total_monto=Coalesce(Sum('total'), Decimal('0')),
        ticket_promedio=Coalesce(Avg('total'), Decimal('0')),
    )

    pedidos_hoy = Pedido.objects.filter(
        creado_el__date=hoy
    ).exclude(estado='ANULADO').aggregate(
        pedidos=Count('id'),
        total=Coalesce(Sum('total'), Decimal('0')),
    )

    mesas_total = Mesa.objects.count()
    mesas_ocupadas = Mesa.objects.filter(estado='OCUPADA').count()

    # Últimos 7 días
    hace_7 = hoy - timedelta(days=6)
    ultimos_7 = (
        Pedido.objects.filter(creado_el__date__range=[hace_7, hoy])
        .exclude(estado='ANULADO')
        .annotate(dia=TruncDate('creado_el'))
        .values('dia')
        .annotate(total=Coalesce(Sum('total'), Decimal('0')))
        .order_by('dia')
    )
    chart_labels = [(hace_7 + timedelta(days=i)).strftime('%d/%m') for i in range(7)]
    datos_map = {d['dia']: float(d['total']) for d in ultimos_7}
    chart_valores = [datos_map.get(hace_7 + timedelta(days=i), 0) for i in range(7)]

    return render(request, 'reportes_restaurante/hub.html', {
        'resumen': resumen, 'pedidos_hoy': pedidos_hoy,
        'mesas_total': mesas_total, 'mesas_ocupadas': mesas_ocupadas,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 1. Ventas por mesa
# ─────────────────────────────────────────────
@login_required
def reporte_ventas_mesa(request):
    desde, hasta = _parse_fechas(request)

    mesas = (
        Pedido.objects.filter(creado_el__date__range=[desde, hasta])
        .exclude(estado='ANULADO')
        .values('mesa__numero', 'mesa__area__nombre')
        .annotate(
            pedidos=Count('id'),
            total=Coalesce(Sum('total'), Decimal('0')),
            promedio=Coalesce(Avg('total'), Decimal('0')),
        )
        .order_by('-total')
    )

    resumen = Pedido.objects.filter(
        creado_el__date__range=[desde, hasta]
    ).exclude(estado='ANULADO').aggregate(
        total=Coalesce(Sum('total'), Decimal('0')),
        pedidos=Count('id'),
    )

    chart_labels = [f"Mesa {m['mesa__numero']}" for m in mesas[:10]]
    chart_valores = [float(m['total']) for m in mesas[:10]]

    return render(request, 'reportes_restaurante/ventas_mesa.html', {
        'mesas': mesas, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 2. Platillos más vendidos
# ─────────────────────────────────────────────
@login_required
def reporte_platillos_vendidos(request):
    desde, hasta = _parse_fechas(request)
    limit = int(request.GET.get('limit', 20))

    platillos = (
        DetallePedido.objects
        .filter(pedido__creado_el__date__range=[desde, hasta])
        .exclude(pedido__estado='ANULADO')
        .values('platillo__nombre', 'platillo__categoria__nombre', 'platillo__precio_venta')
        .annotate(
            cantidad=Coalesce(Sum('cantidad'), 0),
            total=Coalesce(Sum(F('cantidad') * F('precio_unitario')), Decimal('0')),
        )
        .order_by('-cantidad')[:limit]
    )

    resumen = DetallePedido.objects.filter(
        pedido__creado_el__date__range=[desde, hasta]
    ).exclude(pedido__estado='ANULADO').aggregate(
        total_items=Coalesce(Sum('cantidad'), 0),
        total_monto=Coalesce(Sum(F('cantidad') * F('precio_unitario')), Decimal('0')),
    )

    chart_labels = [p['platillo__nombre'][:20] for p in platillos[:10]]
    chart_valores = [int(p['cantidad']) for p in platillos[:10]]

    return render(request, 'reportes_restaurante/platillos_vendidos.html', {
        'platillos': platillos, 'resumen': resumen,
        'desde': desde, 'hasta': hasta, 'limit': limit,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 3. Reporte de caja
# ─────────────────────────────────────────────
@login_required
def reporte_caja(request):
    desde, hasta = _parse_fechas(request)

    cajas = (
        Caja.objects
        .filter(fecha_apertura__date__range=[desde, hasta])
        .select_related('usuario')
        .order_by('-fecha_apertura')
    )

    resumen = cajas.aggregate(
        total_ventas=Coalesce(Sum('total_ventas'), Decimal('0')),
        total_efectivo=Coalesce(Sum('total_efectivo'), Decimal('0')),
        total_tarjeta=Coalesce(Sum('total_tarjeta'), Decimal('0')),
        total_propinas=Coalesce(Sum('total_propinas'), Decimal('0')),
        total_diferencia=Coalesce(Sum('diferencia'), Decimal('0')),
        aperturas=Count('id'),
    )

    return render(request, 'reportes_restaurante/caja.html', {
        'cajas': cajas, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
    })


# ─────────────────────────────────────────────
# 4. Ventas por mesero
# ─────────────────────────────────────────────
@login_required
def reporte_ventas_mesero(request):
    desde, hasta = _parse_fechas(request)

    meseros = (
        Pedido.objects.filter(creado_el__date__range=[desde, hasta])
        .exclude(estado='ANULADO')
        .values('mesero__nombre')
        .annotate(
            pedidos=Count('id'),
            total=Coalesce(Sum('total'), Decimal('0')),
            promedio=Coalesce(Avg('total'), Decimal('0')),
            mesas_atendidas=Count('mesa', distinct=True),
        )
        .order_by('-total')
    )

    resumen = Pedido.objects.filter(
        creado_el__date__range=[desde, hasta]
    ).exclude(estado='ANULADO').aggregate(
        total=Coalesce(Sum('total'), Decimal('0')),
        pedidos=Count('id'),
    )

    chart_labels = [m['mesero__nombre'] for m in meseros]
    chart_valores = [float(m['total']) for m in meseros]

    return render(request, 'reportes_restaurante/ventas_mesero.html', {
        'meseros': meseros, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
    })


# ─────────────────────────────────────────────
# 5. Comandas por área de cocina
# ─────────────────────────────────────────────
@login_required
def reporte_comandas_area(request):
    desde, hasta = _parse_fechas(request)

    areas = (
        Comanda.objects
        .filter(creada_el__date__range=[desde, hasta])
        .values('area_cocina__area_cocina')
        .annotate(
            total_comandas=Count('id'),
            cerradas=Count('id', filter=Q(estado='CERRADA')),
            anuladas=Count('id', filter=Q(estado='ANULADA')),
            en_proceso=Count('id', filter=Q(estado__in=['ENVIADA', 'EN_PREPARACION'])),
        )
        .order_by('-total_comandas')
    )

    resumen = Comanda.objects.filter(
        creada_el__date__range=[desde, hasta]
    ).aggregate(
        total=Count('id'),
        cerradas=Count('id', filter=Q(estado='CERRADA')),
    )

    chart_labels = [a['area_cocina__area_cocina'] or 'Sin área' for a in areas]
    chart_valores = [a['total_comandas'] for a in areas]

    return render(request, 'reportes_restaurante/comandas_area.html', {
        'areas': areas, 'resumen': resumen,
        'desde': desde, 'hasta': hasta,
        'chart_labels': chart_labels, 'chart_valores': chart_valores,
    })
