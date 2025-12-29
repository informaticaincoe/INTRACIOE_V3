from django.contrib import admin

from RESTAURANTE.models import CategoriaMenu, Mesa, Mesero, Platillo

# Register your models here.
admin.site.register(CategoriaMenu)
admin.site.register(Mesero)
admin.site.register(Mesa)
admin.site.register(Platillo)