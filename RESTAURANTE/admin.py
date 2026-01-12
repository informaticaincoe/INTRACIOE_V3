# RESTAURANTE/admin.py
from django.contrib import admin
from RESTAURANTE.models import (
    Area,
    AsignacionMesa,
    CategoriaMenu,
    Mesa,
    Mesero,
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


@admin.register(Platillo)
class PlatilloAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria", "precio_venta", "disponible", "es_preparado")
    list_filter = ("disponible", "es_preparado", "categoria")
    search_fields = ("nombre", "categoria__nombre")
    ordering = ("nombre",)
    autocomplete_fields = ("categoria",)
