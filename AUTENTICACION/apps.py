from django.apps import AppConfig


class AutenticacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AUTENTICACION'

    def ready(self):
        from . import signals  # importa las señales