# AUTENTICACION/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from FE.models import Emisor_fe

from .models import (
    Perfilusuario,
    UsuarioEmisor,
    PasswordResetCode,
    ConfiguracionServidor,
)
# Ajusta el import al nombre real de tu app que contiene Emisor_fe

User = get_user_model()

# --- 1) Asegurar que User tenga un admin con search_fields (NECESARIO para autocomplete_fields hacia user) ---
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # además de lo que ya trae BaseUserAdmin, nos aseguramos de que haya search_fields
    list_display = ("username", "email", "first_name", "last_name", "is_staff")


# --- 2) Asegurar que Emisor_fe tenga admin con search_fields si lo usas en autocomplete_fields ---
# Si Emisor_fe ya está registrado en otra app, lo desregistramos para volver a registrarlo con search_fields
try:
    admin.site.unregister(Emisor_fe)
except admin.sites.NotRegistered:
    pass

@admin.register(Emisor_fe)
class EmisorFeAdmin(admin.ModelAdmin):
    list_display = ("nombre_razon_social", "nit", "nrc", "email")
    #search_fields = ("nombre_razon_social", "nit", "nrc", "email")  # <- requerido por autocomplete_fields
    list_filter = ("tipoContribuyente", "ambiente")
    #autocomplete_fields = ("municipio", "tipoestablecimiento", "tipo_documento", "representante")
    # Si no quieres autocompletar estos, puedes quitarlos; pero search_fields se mantiene.


# --- 3) Resto de admins de AUTENTICACION ---

@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display  = ("user", "code", "created_at", "used")
    list_filter   = ("used", "created_at")
    # Estos search_fields no son estrictamente por E040 (que exige en el destino),
    # pero ayudan para buscar en esta pantalla también:
    #search_fields = ("code", "user__email", "user__username", "user__first_name", "user__last_name")
    autocomplete_fields = ("user",)  # <- ahora OK, porque UserAdmin ya está registrado con search_fields


@admin.register(Perfilusuario)
class PerfilusuarioAdmin(admin.ModelAdmin):
    list_display  = ("user", "nombre", "apellido", "telefono", "fecha_creacion", "emisor_activo")
    list_filter   = ("fecha_creacion",)
    #search_fields = ("user__email", "user__username", "nombre", "apellido", "telefono")
    #autocomplete_fields = ("user", "emisor_activo")  # <- OK: User y Emisor_fe tienen search_fields


@admin.register(UsuarioEmisor)
class UsuarioEmisorAdmin(admin.ModelAdmin):
    list_display  = ("user", "emisor", "activo", "es_predeterminado", "creado")
    list_filter   = ("activo", "es_predeterminado", "creado")
    # IMPORTANTE: aunque E040 se refiere al admin del destino,
    # estos search_fields te permiten buscar aquí también:
    #search_fields = ("user__username", "user__email", "emisor__nombre_razon_social", "emisor__nit")
    #autocomplete_fields = ("user", "emisor")  # <- OK: UserAdmin y EmisorFeAdmin tienen search_fields


@admin.register(ConfiguracionServidor)
class ConfiguracionServidorAdmin(admin.ModelAdmin):
    list_display  = ("clave", "valor", "url", "url_endpoint", "fecha_creacion")
    #search_fields = ("clave", "valor", "url", "url_endpoint", "descripcion")
    list_filter   = ("fecha_creacion",)
