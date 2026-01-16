# RESTAURANTE/admin.py
from django.contrib import admin
from FE.models import FacturaElectronica, Receptor_fe
from RESTAURANTE.models import (
    Area,
    AsignacionMesa,
    Caja,
    CategoriaMenu,
    Cocinero,
    Comanda,
    ComandaItem,
    CuentaPedido,
    DetallePedido,
    Mesa,
    Mesero,
    MovimientosCaja,
    Pedido,
    Platillo,
)

@admin.register(CategoriaMenu)
class CategoriaMenuAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "color")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Mesero)
class MeseroAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo", "nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("codigo", "nombre")
    ordering = ("nombre",)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ("id", "numero", "area", "capacidad", "es_vip", "estado")
    list_filter = ("estado", "es_vip", "area")
    search_fields = ("numero", "area__nombre")
    ordering = ("numero",)
    autocomplete_fields = ("area",)


@admin.register(AsignacionMesa)
class AsignacionMesaAdmin(admin.ModelAdmin):
    list_display = ("id", "mesa", "mesero", "es_fija", "fecha_inicio", "fecha_fin", "activa")
    list_filter = ("activa", "es_fija", "mesa", "mesero")
    search_fields = ("mesa__numero", "mesero__codigo", "mesero__nombre")
    ordering = ("-fecha_inicio",)
    date_hierarchy = "fecha_inicio"
    autocomplete_fields = ("mesa", "mesero")

@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "estado", "fecha_apertura", "fecha_cierre", "total_ventas", "total_efectivo", "total_tarjeta")
    list_filter = ("estado", "fecha_apertura")
    date_hierarchy = "fecha_apertura"

    # ✅ mínimo para que autocomplete_fields funcione (con esto ya pasan los checks)
    search_fields = ("id",)

    # Si quieres que busque por usuario también (ajusta el campo real):
    # search_fields = ("id", "usuario__nombre", "usuario__user__username")
    
@admin.register(MovimientosCaja)
class MovimientosCajaAdmin(admin.ModelAdmin):
    list_display = ("id", "caja", "tipo_movimiento", "monto", "motivo", "fecha")
    list_filter = ("tipo_movimiento", "fecha")
    search_fields = ("motivo", "caja__id")
    autocomplete_fields = ("caja",)

@admin.register(Platillo)
class PlatilloAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria", "precio_venta", "disponible", "es_preparado")
    list_filter = ("disponible", "es_preparado", "categoria")
    search_fields = ("nombre", "categoria__nombre")
    ordering = ("nombre",)
    autocomplete_fields = ("categoria",)

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    autocomplete_fields = ("platillo",)
    fields = (
        "platillo",
        "cantidad",
        "precio_unitario",
        "descuento_pct",
        "aplica_iva",
        "subtotal_linea",
        "descuento_monto",
        "iva_monto",
        "total_linea",
        "notas",
    )
    readonly_fields = ("subtotal_linea", "descuento_monto", "iva_monto", "total_linea")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [DetallePedidoInline]

    list_display = (
        "id",
        "mesa",
        "mesero",
        "estado",
        "creado_el",
        "subtotal",
        "iva_total",
        "propina",
        "total",
        "factura",
    )
    list_filter = ("estado", "mesa", "mesero", "creado_el")
    date_hierarchy = "creado_el"
    search_fields = (
        "id",
        "mesa__numero",
        "mesero__codigo",
        "mesero__nombre",
        "receptor__num_documento",
        "receptor__nombre",
        "factura__numero_control",
    )
    autocomplete_fields = ("mesa", "mesero", "caja")

    # para que no se “rompa” el control de totales desde admin
    readonly_fields = (
        "creado_el",
        "cerrado_el",
        "pagado_el",
        "subtotal",
        "descuento_total",
        "iva_total",
        "total",
    )

    fieldsets = (
        ("Datos del pedido", {
            "fields": ("mesa", "mesero", "estado", "notas")
        }),
        ("Cliente / Caja / Factura", {
            "fields": ("receptor", "caja", "factura")
        }),
        ("Totales", {
            "fields": ("subtotal", "descuento_total", "iva_total", "propina", "total")
        }),
        ("Fechas", {
            "fields": ("creado_el", "cerrado_el", "pagado_el")
        }),
    )

    actions = ("accion_cerrar_pedido", "accion_recalcular_totales")

    def save_model(self, request, obj, form, change):
        """
        - Si cambian estado desde admin, sincroniza mesa.
        - Recalcula totales por seguridad.
        """
        super().save_model(request, obj, form, change)
        try:
            obj.recalcular_totales(save=True)
            obj._sync_estado_mesa()
        except Exception:
            # no rompas admin por un cálculo; si quieres log, lo agregas
            pass

    @admin.action(description="Cerrar pedido (ABIERTO -> CERRADO) y poner mesa en PENDIENTE_PAGO")
    def accion_cerrar_pedido(self, request, queryset):
        count = 0
        for pedido in queryset.select_related("mesa").all():
            if pedido.estado == "ABIERTO":
                pedido.cerrar()
                count += 1
        self.message_user(request, f"Pedidos cerrados: {count}")

    @admin.action(description="Recalcular totales del pedido")
    def accion_recalcular_totales(self, request, queryset):
        count = 0
        for pedido in queryset.all():
            pedido.recalcular_totales(save=True)
            count += 1
        self.message_user(request, f"Totales recalculados para {count} pedidos.")


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pedido",
        "platillo",
        "cuenta",
        "cantidad",
        "precio_unitario",
        "descuento_pct",
        "aplica_iva",
        "total_linea",
        "creado_el",
    )
    list_filter = ("aplica_iva", "creado_el")
    search_fields = ("pedido__id", "pedido__mesa__numero", "platillo__nombre", "platillo__codigo")
    autocomplete_fields = ("pedido", "platillo", "cuenta")
    readonly_fields = ("subtotal_linea", "descuento_monto", "iva_monto", "total_linea", "creado_el")
    
@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pedido",
        "numero",
        "estado",
        "creada_el",
        "iniciada_el",
        "cerrada_el",
    )
    list_filter = ("numero", "estado", "pedido")
    search_fields = ("pedido__id", "pedido__mesa__numero")
    readonly_fields = ("creada_el", "iniciada_el", "cerrada_el")
    
@admin.register(ComandaItem)
class ComandaItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "comanda",
        "detalle_pedido",
        "nombre",
        "cantidad",
        "notas",
        "enviado_el",
        "iniciado_el",
        "entregado_el",
        "listo_el"
    )
    list_filter = ("comanda", "detalle_pedido", "nombre")
    search_fields = ("pedido__id", "pedido__mesa__numero")
    autocomplete_fields = ("comanda", "detalle_pedido")
    readonly_fields = ("enviado_el", "iniciado_el", "entregado_el", "listo_el")
    
@admin.register(Cocinero)
class CocineroAdmin(admin.ModelAdmin):
    list_display = ("nombre", "pin", "activo")
    search_fields = ("nombre", "pin")
    list_filter = ("activo",)
    
@admin.register(CuentaPedido)
class CuentaPedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pedido",
        "nombre",
        "estado",
        "creado_el",
        "cerrado_el",
        "pagado_el",
        "subtotal",
        "total",
        "propina"
    )
    list_filter = ("pedido", "nombre", "estado")
    search_fields = ("pedido__id", "pedido__mesa__numero")
    readonly_fields = ("creado_el", "cerrado_el", "pagado_el", "subtotal", "total", "propina")
    