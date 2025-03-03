from django.apps import AppConfig


class DteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dte'
    verbose_name = '01 Facturación Electrónica'  # Nombre personalizado en el admin