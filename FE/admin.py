from django.contrib import admin
from .models import Token_data

# Register your models here.

#admin para el modelo token_data

class Token_dataAdmin(admin.ModelAdmin):
    list_display = ('token', 'nit_empresa', 'created_at')
    search_fields = ('token', 'nit_empresa')
    #list_filter = ('created_at')

admin.site.register(Token_data, Token_dataAdmin)
