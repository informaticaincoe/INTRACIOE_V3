from django.contrib import admin
from .models import ConfiguracionContable, CuentaContable


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
