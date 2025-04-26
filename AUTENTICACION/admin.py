from django.contrib import admin

# Register your models here.
from .models import ConfiguracionServidor  # Asegúrate de importar el modelo correctamente

admin.site.register(ConfiguracionServidor)
