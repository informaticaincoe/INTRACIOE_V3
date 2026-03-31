from django.contrib import admin
from .models import (
    ConfiguracionContable, CuentaContable,
    AsientoContable, LineaAsiento,
    CuentaPorCobrar, PagoCobro,
    CuentaPorPagar, PagoPagar,
)


@admin.register(ConfiguracionContable)
class ConfiguracionContableAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Ventas', {
            'fields': ('cuenta_ingresos_ventas', 'cuenta_cxc', 'cuenta_iva_debito_fiscal'),
        }),
        ('Compras', {
            'fields': ('cuenta_compras', 'cuenta_cxp', 'cuenta_iva_credito_fiscal', 'cuenta_inventario'),
        }),
        ('Efectivo', {
            'fields': ('cuenta_caja', 'cuenta_banco'),
        }),
        ('Configuración', {
            'fields': ('dias_vencimiento_cxc', 'dias_vencimiento_cxp', 'auto_confirmar_asientos'),
        }),
    )

    def has_add_permission(self, request):
        return not ConfiguracionContable.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo', 'naturaleza', 'nivel', 'activa')
    list_filter = ('tipo', 'naturaleza', 'nivel', 'activa')
    search_fields = ('codigo', 'nombre')
    ordering = ('codigo',)


class LineaAsientoInline(admin.TabularInline):
    model = LineaAsiento
    extra = 1
    fields = ('cuenta', 'descripcion', 'debe', 'haber')
    autocomplete_fields = ('cuenta',)


@admin.register(AsientoContable)
class AsientoContableAdmin(admin.ModelAdmin):
    list_display = ('numero', 'fecha', 'periodo', 'concepto', 'estado', 'total_debe', 'total_haber')
    list_filter = ('estado', 'periodo')
    search_fields = ('numero', 'concepto')
    ordering = ('-fecha', '-numero')
    inlines = [LineaAsientoInline]
    readonly_fields = ('numero', 'creado_en')

    @admin.display(description="Total Debe")
    def total_debe(self, obj):
        return f"${obj.total_debe:,.2f}"

    @admin.display(description="Total Haber")
    def total_haber(self, obj):
        return f"${obj.total_haber:,.2f}"


class PagoCobroInline(admin.TabularInline):
    model = PagoCobro
    extra = 0
    fields = ('fecha', 'monto', 'forma_pago', 'referencia')
    readonly_fields = ('fecha',)


@admin.register(CuentaPorCobrar)
class CuentaPorCobrarAdmin(admin.ModelAdmin):
    list_display = ('id', 'receptor_nombre', 'fecha_emision', 'fecha_vencimiento', 'monto_original', 'estado', 'esta_vencida_display')
    list_filter = ('estado',)
    search_fields = ('receptor__nombre', 'receptor__num_documento')
    ordering = ('-fecha_emision',)
    inlines = [PagoCobroInline]

    @admin.display(description="Cliente")
    def receptor_nombre(self, obj):
        return obj.receptor.nombre if obj.receptor else "—"

    @admin.display(boolean=True, description="Vencida")
    def esta_vencida_display(self, obj):
        return obj.esta_vencida


@admin.register(PagoCobro)
class PagoCobroAdmin(admin.ModelAdmin):
    list_display = ('id', 'cuenta_pagar', 'fecha', 'monto', 'forma_pago', 'referencia')
    list_filter = ('forma_pago', 'fecha')
    ordering = ('-fecha',)

    @admin.display(description="Cuenta")
    def cuenta_pagar(self, obj):
        return f"CxC #{obj.cuenta_pagar_id}"


class PagoPagarInline(admin.TabularInline):
    model = PagoPagar
    extra = 0
    fields = ('fecha', 'monto', 'forma_pago', 'referencia')
    readonly_fields = ('fecha',)


@admin.register(CuentaPorPagar)
class CuentaPorPagarAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor_nombre', 'fecha_emision', 'fecha_vencimiento', 'monto_original', 'estado', 'esta_vencida_display')
    list_filter = ('estado',)
    search_fields = ('proveedor__nombre', 'proveedor__num_documento')
    ordering = ('-fecha_emision',)
    inlines = [PagoPagarInline]

    @admin.display(description="Proveedor")
    def proveedor_nombre(self, obj):
        return obj.proveedor.nombre if obj.proveedor else "—"

    @admin.display(boolean=True, description="Vencida")
    def esta_vencida_display(self, obj):
        return obj.esta_vencida


@admin.register(PagoPagar)
class PagoPagarAdmin(admin.ModelAdmin):
    list_display = ('id', 'cuenta_display', 'fecha', 'monto', 'forma_pago', 'referencia')
    list_filter = ('forma_pago', 'fecha')
    ordering = ('-fecha',)

    @admin.display(description="Cuenta")
    def cuenta_display(self, obj):
        return f"CxP #{obj.cuenta_pagar_id}"
