# FE/views.py
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, F, DecimalField
from django.db.models.functions import TruncMonth, Coalesce
from django.shortcuts import render
from decimal import Decimal
from django.db.models import Q

# Modelos que ya tienes
from FE.models import FacturaElectronica, DetalleFactura, Receptor_fe
# Intento de modelos comunes (cámbialos si usas otros)
try:
    from INVENTARIO.models import Producto  # TODO: ajusta si tu app/modelo tiene otro nombre
except Exception:
    Producto = None

try:
    from INVENTARIO.models import Compra  # TODO
except Exception:
    Compra = None


def _pick_field(model, candidates):
    """Devuelve el primer field existente en el modelo."""
    if not model:
        return None
    names = {f.name for f in model._meta.get_fields()}
    for name in candidates:
        if name in names:
            return name
    return None


def _last_n_months(n=6):
    """Lista [(año, mes, date-1°), …] de los últimos n meses (incluye el actual)."""
    today = timezone.localdate()
    y, m = today.year, today.month
    out = []
    for _ in range(n):
        out.append((y, m, timezone.datetime(y, m, 1).date()))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return list(reversed(out))


@login_required
def dashboard(request):
    # ===== Meses base =====
    months = _last_n_months(6)
    labels = [timezone.datetime(y, m, 1).strftime("%b %Y") for (y, m, _d) in months]

    # ===== Ventas (FacturaElectronica) por mes =====
    ventas_data = [0] * len(months)
    total_ventas = 0
    total_facturas = 0

    fac_date_field = _pick_field(
        FacturaElectronica,
        ["fecha_emision", "fecha", "fecha_generacion", "created_at", "created", "fecha_creacion", "timestamp"],
    )
    if fac_date_field:
        qs = (
            FacturaElectronica.objects
            .annotate(m=TruncMonth(F(fac_date_field)))
            .values("m")
            .annotate(
                total=Coalesce(Sum("total_pagar"), Decimal("0.00"), output_field=DecimalField()),
                cnt=Count("id")
            )
            .order_by("m")
        )
        # Mapear por YYYY-MM
        by_month = {row["m"].strftime("%Y-%m"): (float(row["total"]), int(row["cnt"])) for row in qs if row["m"]}
        total_facturas = sum(v[1] for v in by_month.values())
        for i, (y, m, _d) in enumerate(months):
            key = f"{y:04d}-{m:02d}"
            ventas_data[i] = round(by_month.get(key, (0.0, 0))[0], 2)
        total_ventas = round(sum(ventas_data), 2)
    else:
        total_facturas = FacturaElectronica.objects.count()
        total_ventas = float(FacturaElectronica.objects.aggregate(s=Coalesce(Sum("total_pagar"), 0.0))["s"] or 0)

    # ===== Compras por mes (si tienes modelo Compra) =====
    compras_labels = labels[:]
    compras_data = [0] * len(months)
    if Compra:
        comp_date_field = _pick_field(
            Compra,
            ["fecha", "fecha_emision", "created_at", "created", "fecha_creacion", "timestamp"],
        )
        if comp_date_field:
            qs = (FacturaElectronica.objects
                .annotate(m=TruncMonth("fecha_emision"))
                .values("m")
                .annotate(
                    total=Coalesce(
                        Sum("total_pagar", output_field=DecimalField()),
                        Decimal("0.00"),
                        output_field=DecimalField()
                    ),
                    cnt=Count("id")
                )
                .order_by("m")
            )
            by_month = {
                row["m"].strftime("%Y-%m"): float(row["total"] or 0)
                for row in qs if row["m"]
            }
            for i, (y, m, _d) in enumerate(months):
                compras_data[i] = round(by_month.get(f"{y:04d}-{m:02d}", 0.0), 2)

    # ===== Clientes por mes =====
    clientes_labels = labels[:]
    clientes_data = [0] * len(months)
    cli_date_field = _pick_field(Receptor_fe, ["created_at", "created", "fecha_creacion", "fecha_registro"])
    if cli_date_field:
        qs = (
            Receptor_fe.objects
            .annotate(m=TruncMonth(F(cli_date_field)))
            .values("m")
            .annotate(c=Count("id"))
            .order_by("m")
        )
        by_month = {row["m"].strftime("%Y-%m"): int(row["c"]) for row in qs if row["m"]}
        for i, (y, m, _d) in enumerate(months):
            clientes_data[i] = by_month.get(f"{y:04d}-{m:02d}", 0)
    total_clientes = Receptor_fe.objects.count()

    # ===== Inventario (top categorías o valor) =====
    inv_labels, inv_data = [], []
    inventario_valor_total = 0.0
    if Producto:
        # Campos típicos
        stock_field = _pick_field(Producto, ["existencia", "existencias", "stock", "cantidad_disponible"])
        precio_field = _pick_field(Producto, ["precio", "precio_venta", "preunitario", "precio_sugerido"])
        categoria_field = _pick_field(Producto, ["categoria", "categoria__nombre", "familia", "grupo"])

        try:
            if stock_field and precio_field:
                # Valor total
                inventario_valor_total = float(
                    Producto.objects.aggregate(
                        v=Coalesce(Sum(F(stock_field) * F(precio_field)), 0.0)
                    )["v"] or 0
                )
            # Top por categoría (si hay)
            if categoria_field and stock_field:
                # Si categoria es FK usamos categoria__nombre; si no, el mismo field
                cat_expr = F(categoria_field) if "__" in categoria_field else F(categoria_field)
                qs = (
                    Producto.objects
                    .values(categoria_field)
                    .annotate(total=Coalesce(Sum(stock_field), 0))
                    .order_by("-total")[:6]
                )
                inv_labels = [str(row[categoria_field]) or "—" for row in qs]
                inv_data = [int(row["total"] or 0) for row in qs]
        except Exception:
            pass

    # ===== Facturación por estado =====
    fact_estado_labels = ["Aprobadas", "Rechazadas", "Pendientes"]

    # 1) Aprobadas:
    #   - sello_recepcion NO es null ni cadena vacía
    #   - NO tienen evento de invalidación asociado
    aprobadas = (
        FacturaElectronica.objects
        .filter(
            Q(sello_recepcion__isnull=False) & ~Q(sello_recepcion=""),
            dte_invalidacion__isnull=True,
        )
        .count()
    )

    # 2) Rechazadas:
    #   - sello_recepcion vacío (NULL o "")
    #   - opcional: ya están firmadas para no mezclar con pendientes
    rechazadas = (
        FacturaElectronica.objects
        .filter(
            Q(sello_recepcion__isnull=True) | Q(sello_recepcion=""),
            firmado=True,
        )
        .count()
    )

    # 3) Pendientes:
    #   - firmado == False
    pendientes = FacturaElectronica.objects.filter(firmado=False).count()

    fact_estado_data = [aprobadas, rechazadas, pendientes]

    # ===== Top 5 productos vendidos =====
    top_prod_labels, top_prod_data = [], []
    try:
        # asumimos campo 'cantidad' en DetalleFactura y FK 'producto'
        qs = (
            DetalleFactura.objects
            .values("producto__descripcion")  # ajusta a producto__nombre si aplica
            .annotate(c=Coalesce(Sum("cantidad"), 0))
            .order_by("-c")[:5]
        )
        top_prod_labels = [row["producto__descripcion"] or "—" for row in qs]
        top_prod_data = [int(row["c"] or 0) for row in qs]
    except Exception:
        pass

    context = {
        # KPIs
        "total_ventas": total_ventas,
        "total_facturas": total_facturas,
        "total_clientes": total_clientes,
        "inventario_valor_total": inventario_valor_total,

        # Series
        "ventas_mes_labels": labels,
        "ventas_mes_data": ventas_data,

        "compras_mes_labels": compras_labels,
        "compras_mes_data": compras_data,

        "clientes_mes_labels": clientes_labels,
        "clientes_mes_data": clientes_data,

        "inv_labels": inv_labels,
        "inv_data": inv_data,

        "fact_estado_labels": fact_estado_labels,
        "fact_estado_data": fact_estado_data,

        "top_prod_labels": top_prod_labels,
        "top_prod_data": top_prod_data,
    }
    return render(request, "base.html", context)
