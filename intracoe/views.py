# FE/views.py
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, F, DecimalField,ExpressionWrapper, Value
from django.db.models.functions import TruncMonth, Coalesce
from django.shortcuts import render
from decimal import Decimal
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

# Modelos que ya tienes
from FE.models import Emisor_fe, FacturaElectronica, DetalleFactura, Receptor_fe
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


def _months_between(desde, hasta):
    """Lista [(año, mes, date-1°), …] entre dos fechas."""
    out = []
    y, m = desde.year, desde.month
    while date(y, m, 1) <= hasta:
        out.append((y, m, date(y, m, 1)))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def _parse_dash_filters(request):
    """Extrae periodo, desde, hasta del GET y retorna (desde, hasta, periodo_key)."""
    from dateutil.relativedelta import relativedelta

    periodo = request.GET.get('periodo', '6m')
    desde_str = request.GET.get('desde', '')
    hasta_str = request.GET.get('hasta', '')
    today = timezone.localdate()

    # Si hay fechas manuales, usarlas
    if desde_str and hasta_str:
        try:
            desde = date.fromisoformat(desde_str)
            hasta = date.fromisoformat(hasta_str)
            return desde, hasta, 'custom'
        except ValueError:
            pass

    # Periodos predefinidos
    periods = {
        '7d':  today - timezone.timedelta(days=6),
        '30d': today - timezone.timedelta(days=29),
        '3m':  (today - relativedelta(months=2)).replace(day=1),
        '6m':  (today - relativedelta(months=5)).replace(day=1),
        '12m': (today - relativedelta(months=11)).replace(day=1),
        'anio': date(today.year, 1, 1),
    }
    desde = periods.get(periodo, periods['6m'])
    return desde, today, periodo


@login_required
def dashboard(request):
    desde, hasta, periodo_key = _parse_dash_filters(request)

    # ===== Meses base =====
    months = _months_between(desde, hasta)
    labels = [timezone.datetime(y, m, 1).strftime("%b %Y") for (y, m, _d) in months]

    # ===== Filtro base de fecha para facturas =====
    fac_date_field = _pick_field(
        FacturaElectronica,
        ["fecha_emision", "fecha", "fecha_generacion", "created_at", "created", "fecha_creacion", "timestamp"],
    )
    fac_date_filter = {}
    if fac_date_field:
        fac_date_filter = {f"{fac_date_field}__gte": desde, f"{fac_date_field}__lte": hasta}

    # ===== Ventas (FacturaElectronica) por mes =====
    ventas_data = [0] * len(months)
    total_ventas = 0
    total_facturas = 0

    if fac_date_field:
        qs = (
            FacturaElectronica.objects.filter(**fac_date_filter)
            .annotate(m=TruncMonth(F(fac_date_field)))
            .values("m")
            .annotate(
                total=Coalesce(Sum("total_pagar"), Decimal("0.00"), output_field=DecimalField()),
                cnt=Count("id")
            )
            .order_by("m")
        )
        by_month = {row["m"].strftime("%Y-%m"): (float(row["total"]), int(row["cnt"])) for row in qs if row["m"]}
        total_facturas = sum(v[1] for v in by_month.values())
        for i, (y, m, _d) in enumerate(months):
            key = f"{y:04d}-{m:02d}"
            ventas_data[i] = round(by_month.get(key, (0.0, 0))[0], 2)
        total_ventas = round(sum(ventas_data), 2)
    else:
        total_facturas = FacturaElectronica.objects.count()
        total_ventas = float(FacturaElectronica.objects.aggregate(s=Coalesce(Sum("total_pagar"), 0.0))["s"] or 0)

    # ===== Compras por mes =====
    compras_labels = labels[:]
    compras_data = [0] * len(months)
    if Compra:
        comp_date_field = _pick_field(
            Compra, ["fecha", "fecha_emision", "created_at", "created", "fecha_creacion", "timestamp"],
        )
        if comp_date_field:
            comp_filter = {f"{comp_date_field}__gte": desde, f"{comp_date_field}__lte": hasta}
            qs = (
                Compra.objects.filter(**comp_filter)
                .annotate(m=TruncMonth(F(comp_date_field)))
                .values("m")
                .annotate(
                    total=Coalesce(Sum("total", output_field=DecimalField()), Decimal("0.00"),
                                   output_field=DecimalField()),
                )
                .order_by("m")
            )
            by_month = {row["m"].strftime("%Y-%m"): float(row["total"] or 0) for row in qs if row["m"]}
            for i, (y, m, _d) in enumerate(months):
                compras_data[i] = round(by_month.get(f"{y:04d}-{m:02d}", 0.0), 2)

    # ===== Clientes por mes =====
    clientes_labels = labels[:]
    clientes_data = [0] * len(months)
    cli_date_field = _pick_field(Receptor_fe, ["created_at", "created", "fecha_creacion", "fecha_registro"])

    if cli_date_field:
        cli_filter = {f"{cli_date_field}__gte": desde, f"{cli_date_field}__lte": hasta}
        qs = (
            Receptor_fe.objects.filter(**cli_filter)
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
        stock_field = _pick_field(Producto, ["existencia", "existencias", "stock", "cantidad_disponible"])
        precio_field = _pick_field(Producto, ["preunitario", "precio", "precio_venta", "precio_sugerido"])
        categoria_field = _pick_field(Producto, ["categoria", "categoria__nombre", "familia", "grupo"])
        try:
            if stock_field and precio_field:
                valor_expr = ExpressionWrapper(
                    F(stock_field) * F(precio_field),
                    output_field=DecimalField(max_digits=20, decimal_places=2),
                )
                agg = Producto.objects.aggregate(
                    v=Coalesce(Sum(valor_expr, output_field=DecimalField(max_digits=20, decimal_places=2)),
                               Value(Decimal("0.00")), output_field=DecimalField(max_digits=20, decimal_places=2))
                )
                inventario_valor_total = float(agg["v"] or Decimal("0.00"))

            if categoria_field and stock_field:
                cat_value_field = "categoria__nombre" if categoria_field == "categoria" else categoria_field
                qs = (
                    Producto.objects.values(cat_value_field)
                    .annotate(total=Coalesce(Sum(stock_field), 0))
                    .order_by("-total")[:6]
                )
                inv_labels = [str(row[cat_value_field]) or "—" for row in qs]
                inv_data = [int(row["total"] or 0) for row in qs]
        except Exception:
            pass

    # ===== Facturación por estado (dentro del rango) =====
    fact_estado_labels = ["Aprobadas", "Rechazadas", "Pendientes"]
    fac_qs = FacturaElectronica.objects.filter(**fac_date_filter) if fac_date_filter else FacturaElectronica.objects

    aprobadas = fac_qs.filter(
        Q(sello_recepcion__isnull=False) & ~Q(sello_recepcion=""),
        dte_invalidacion__isnull=True,
    ).count()
    rechazadas = fac_qs.filter(
        Q(sello_recepcion__isnull=True) | Q(sello_recepcion=""),
        firmado=True,
    ).count()
    pendientes = fac_qs.filter(firmado=False).count()
    fact_estado_data = [aprobadas, rechazadas, pendientes]

    # ===== Top 5 productos vendidos (dentro del rango) =====
    top_prod_labels, top_prod_data = [], []
    try:
        det_qs = DetalleFactura.objects.all()
        if fac_date_filter:
            det_filter = {f"factura__{k}": v for k, v in fac_date_filter.items()}
            det_qs = det_qs.filter(**det_filter)
        qs = (
            det_qs.values("producto__codigo")
            .annotate(c=Coalesce(Sum("cantidad"), 0))
            .order_by("-c")[:5]
        )
        top_prod_labels = [row["producto__codigo"] or "—" for row in qs]
        top_prod_data = [int(row["c"] or 0) for row in qs]
    except Exception:
        pass

    context = {
        # Filtros
        "periodo_key": periodo_key,
        "filtro_desde": desde.isoformat(),
        "filtro_hasta": hasta.isoformat(),

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


class CustomLoginView(LoginView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        mode = request.POST.get('login_mode')
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        if mode == 'staff':
            user = authenticate(request, username=identifier)
            if user:
                login(request, user)
                return self.form_valid(None) # Redirige según el success_url
        
        # Si es admin o falló el staff, usamos el comportamiento normal
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        # Redirección inteligente por rol
        role = getattr(user, 'role', None)
        if role == 'cocinero': return reverse_lazy('comanda-cocina')
        if role == 'mesero': return reverse_lazy('mesas-lista')
        return super().get_success_url()
    
def staff_pin_login(request):
    if request.method == "POST":
        pin = request.POST.get("username")
        print(f"DEBUG: Intentando login con PIN: {pin}") # Mira tu consola
        
        # Especificamos el backend explícitamente para evitar conflictos
        # Forma correcta de llamar al backend específico
        user = authenticate(
            request, 
            username=pin, 
            backend='intracoe.backends_login.MultiRoleBackend'
        )
        
        print(f"DEBUG: User: {user}") # Mira tu consola
        
        if user is not None:
            login(request, user)
            print(f"DEBUG: Login exitoso para {user.username} con rol {user.role}")
            
            if user.role == 'cocinero':
                return redirect('comanda-cocina')
            elif user.role == 'mesero':
                return redirect('mesas-lista')
            elif user.role == 'cajero':
                return redirect('index')
            return redirect('index')
        else:
            print("DEBUG: Autenticación fallida")
            print("PIN ", pin)
            
            messages.error(request, "PIN incorrecto o empleado inactivo.", extra_tags="usuario_no_encontrado")

    return render(request, "staff_login.html")


# ── Páginas de error ──
def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)

def error_403(request, exception):
    return render(request, '403.html', status=403)