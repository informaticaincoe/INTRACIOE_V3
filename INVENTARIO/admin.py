from django.contrib import admin
from .models import Producto
from .models import TipoItem
from .models import TipoValor, Tributo, TipoTributo, Impuesto, Almacen
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