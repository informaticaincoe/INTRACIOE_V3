# AUTENTICACION/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from FE.models import Emisor_fe

from .models import (
    EmailProfile,
    Funcionalidad,
    Perfilusuario,
    UsuarioEmisor,
    PasswordResetCode,
    ConfiguracionServidor,
    Plan,
    Suscripcion,
    User,
)
# Ajusta el import al nombre real de tu app que contiene Emisor_fe

User = get_user_model()

# --- 1) Asegurar que User tenga un admin con search_fields (NECESARIO para autocomplete_fields hacia user) ---
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     # además de lo que ya trae BaseUserAdmin, nos aseguramos de que haya search_fields
#     list_display = ("username", "email", "first_name", "last_name", "is_staff")


# --- 2) Asegurar que Emisor_fe tenga admin con search_fields si lo usas en autocomplete_fields ---
# Si Emisor_fe ya está registrado en otra app, lo desregistramos para volver a registrarlo con search_fields
try:
    admin.site.unregister(Emisor_fe)
except admin.sites.NotRegistered:
    pass


@admin.register(EmailProfile)
class EmailProfileAdmin(admin.ModelAdmin):
    list_display = ("nombre", "scope", "host", "port", "use_ssl", "use_tls", "username", "is_active", "updated_at")
    list_filter  = ("scope", "is_active", "use_ssl", "use_tls")
    search_fields= ("nombre", "host", "username", "from_email")

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

@admin.register(Funcionalidad)
class FuncionalidadAdmin(admin.ModelAdmin):
    list_display = ("clave", "nombre", "modulo", "icono")
    list_filter = ("modulo",)
    search_fields = ("clave", "nombre")
    ordering = ("modulo", "nombre")


from django.forms import CheckboxSelectMultiple, ModelMultipleChoiceField, ModelForm
from AUTENTICACION.models import Funcionalidad as FuncionalidadModel, MODULO_CHOICES


class GroupedCheckboxWidget(CheckboxSelectMultiple):
    """Checkbox widget que agrupa las opciones por módulo."""
    template_name = 'admin/grouped_checkbox.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Agrupar opciones por módulo
        grouped = {}
        modulo_labels = dict(MODULO_CHOICES)
        for func in FuncionalidadModel.objects.all().order_by('modulo', 'nombre'):
            label = modulo_labels.get(func.modulo, func.modulo)
            grouped.setdefault(label, []).append(func)
        context['widget']['grouped'] = grouped
        return context


class PlanForm(ModelForm):
    funcionalidades = ModelMultipleChoiceField(
        queryset=FuncionalidadModel.objects.all().order_by('modulo', 'nombre'),
        widget=CheckboxSelectMultiple,
        required=False,
        label="Funcionalidades incluidas",
    )

    class Meta:
        model = Plan
        fields = '__all__'


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    form = PlanForm
    list_display = (
        "nombre", "tiene_facturacion", "tiene_ventas", "tiene_compras",
        "tiene_inventario", "tiene_contabilidad", "tiene_rrhh", "tiene_restaurante",
        "total_funcionalidades",
    )
    search_fields = ("nombre",)
    fieldsets = (
        (None, {"fields": ("nombre", "descripcion")}),
        ("Módulos habilitados", {"fields": (
            "tiene_facturacion", "tiene_ventas", "tiene_compras",
            "tiene_inventario", "tiene_contabilidad", "tiene_rrhh", "tiene_restaurante",
        )}),
        ("Funcionalidades detalladas", {
            "description": "Marque las funcionalidades específicas incluidas en este plan. "
                           "Solo se mostrarán las opciones de menú correspondientes.",
            "fields": ("funcionalidades",),
            "classes": ("wide",),
        }),
    )

    class Media:
        css = {"all": ()}
        js = ()

    @admin.display(description="Funcionalidades")
    def total_funcionalidades(self, obj):
        return obj.funcionalidades.count()


@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display  = ("emisor", "plan", "fecha_inicio", "fecha_fin", "activo", "esta_vigente")
    list_filter   = ("activo", "plan")
    search_fields = ("emisor__nombre_razon_social", "emisor__nit")

    @admin.display(boolean=True, description="Vigente")
    def esta_vigente(self, obj):
        return obj.esta_vigente()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Rol en el sistema", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser")