from django.contrib import admin
from .models import AjusteInventario, Compra, DetalleCompra, DetalleDevolucionCompra, DetalleDevolucionVenta, DevolucionCompra, DevolucionVenta, NotaCredito, Producto, ProductoProveedor, Proveedor
from .models import TipoItem
from .models import TipoValor, Tributo, TipoTributo, Impuesto, Almacen, MovimientoInventario
# Register your models here.

@admin.register(Almacen)
class AllmacenAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'responsable')
    search_fields = ('nombre', 'ubicacion', 'responsable')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(Impuesto)
class ImpuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'porcentaje')
    search_fields = ('nombre', 'porcentaje')
    
@admin.register(TipoItem)
class TipoItemAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')
    
@admin.register(TipoValor)
class TipoValor(admin.ModelAdmin):
    list_display = ('id', 'descripcion')
    search_fields = ('id','descripcion')

@admin.register(Tributo)
class Tributo(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'descripcion', 'valor_tributo','tipo_valor')
    search_fields = ('id', 'codigo', 'descripcion')
    
@admin.register(TipoTributo)
class TipoTributo(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'descripcion')
    search_fields = ('id', 'codigo', 'descripcion')

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'num_documento', 'contacto', 'telefono', 'email')
    search_fields = ('nombre', 'num_documento')

@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'unidad_medida', 'preunitario')
    search_fields = ('codigo', 'descripcion')

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha', 'total', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('proveedor__nombre',)

@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('compra', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('compra', 'producto')
    search_fields = ('producto__descripcion',)

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'almacen', 'tipo', 'cantidad', 'fecha', 'referencia')
    list_filter = ('tipo', 'almacen', 'fecha')
    search_fields = ('producto__descripcion', 'referencia')

@admin.register(AjusteInventario)
class AjusteInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'almacen', 'cantidad_ajustada', 'motivo', 'fecha', 'usuario')
    list_filter = ('fecha', 'usuario')
    search_fields = ('motivo',)

@admin.register(DevolucionVenta)
class DevolucionVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'num_factura', 'fecha', 'estado', 'usuario')
    list_filter = ('estado', 'fecha')
    search_fields = ('num_factura', 'usuario')

@admin.register(DetalleDevolucionVenta)
class DetalleDevolucionVentaAdmin(admin.ModelAdmin):
    list_display = ('devolucion', 'producto', 'cantidad', 'motivo_detalle')
    search_fields = ('producto__descripcion', 'motivo_detalle')

@admin.register(NotaCredito)
class NotaCreditoAdmin(admin.ModelAdmin):
    list_display = ('id', 'devolucion', 'monto', 'fecha', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('devolucion__id',)

@admin.register(DevolucionCompra)
class DevolucionCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'compra', 'fecha', 'estado', 'usuario')
    list_filter = ('estado', 'fecha')
    search_fields = ('compra__id', 'usuario')

@admin.register(DetalleDevolucionCompra)
class DetalleDevolucionCompraAdmin(admin.ModelAdmin):
    list_display = ('devolucion', 'producto', 'cantidad', 'motivo_detalle')
    search_fields = ('producto__descripcion', 'motivo_detalle')
