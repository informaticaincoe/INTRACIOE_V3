from django.apps import AppConfig


class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'INVENTARIO'

    def ready(self):
        # Importa tu módulo de señales para que Django lo registre
        import INVENTARIO.signals

