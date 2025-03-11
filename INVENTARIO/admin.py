from django.contrib import admin
from .models import Producto
from .models import TipoItem
# Register your models here.


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')
    
@admin.register(TipoItem)
class TipoItemAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')