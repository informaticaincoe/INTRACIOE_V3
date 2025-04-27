from django.contrib import admin
from .models import Token_data
from django import forms
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
from .models import (INCOTERMS, ActividadEconomica, NumeroControl, FacturaElectronica, Emisor_fe, 
                           OtrosDicumentosAsociado, Pais, Receptor_fe, Municipio, Departamento, Tipo_dte, 
                           Ambiente, Modelofacturacion, TipoDocContingencia, TipoDomicilioFiscal, TipoDonacion, 
                           TipoInvalidacion, TipoPersona, TipoTransmision, TipoContingencia, TipoRetencionIVAMH, 
                           TipoGeneracionDocumento, TipoTransporte, TiposDocIDReceptor, TiposEstablecimientos, 
                           TiposServicio_Medico, CondicionOperacion, FormasPago, Plazo,
                            Descuento, DetalleFactura, TipoMoneda, TipoUnidadMedida, EventoInvalidacion, EventoContingencia, LoteContingencia, representanteEmisor)


# Lista de todos los modelos a registrar
models = [
    OtrosDicumentosAsociado, TiposDocIDReceptor, Pais, TipoDocContingencia, TipoInvalidacion,
    TipoDonacion, TipoPersona, TipoTransporte, INCOTERMS, TipoDomicilioFiscal, Descuento,
    TipoMoneda, TipoUnidadMedida,
]

@admin.register(LoteContingencia)
class LoteContingencia(admin.ModelAdmin):
    list_display = ('id', 'recibido_mh')
    
@admin.register(EventoContingencia)
class EventoContingencia(admin.ModelAdmin):
    list_display = ('id', 'codigo_generacion', 'sello_recepcion', 'finalizado', 'recibido_mh', 'rechazado', 'fecha_transmision', 'fecha_modificacion', 'hora_modificacion')
    search_fields = ('codigo_generacion', 'sello_recepcion')

@admin.register(EventoInvalidacion)
class EventoInvalidacion(admin.ModelAdmin):
    list_display = ('id', 'factura', 'codigo_generacion_r', 'tipo_invalidacion', 'motivo_anulacion', 'nombre_solicita', 'tipo_documento_solicita', 'hora_anulacion', 'fecha_anulacion')
    search_fields = ('factura__numero_factura', 'codigo_generacion_r')
    
@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'factura', 'producto', 'cantidad', 'precio_unitario')
    search_fields = ('factura__numero_factura', 'producto__nombre')
    

@admin.register(NumeroControl)
class NumeroControlAdmin(admin.ModelAdmin):
    list_display = ('anio', 'secuencia', 'tipo_dte')
    ordering = ('-anio',)
    search_fields = ('anio',)


@admin.register(FacturaElectronica)
class FacturaElectronicaAdmin(admin.ModelAdmin):
    list_display = (
        'numero_control',
        'codigo_generacion',
        'fecha_emision',
        'hora_emision',
        'firmado',
    )
    list_filter = ('firmado', 'fecha_emision')
    search_fields = ('numero_control', 'codigo_generacion')
    readonly_fields = ('numero_control', 'codigo_generacion', 'fecha_emision', 'hora_emision', 'fecha_modificacion', 'hora_modificacion')
    # Excluir el campo 'id' ya que no es editable y no forma parte del formulario
    fields = [f.name for f in FacturaElectronica._meta.fields if f.name != "id"]

    
class ActividadEconomicaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')  # Agregar campo de búsqueda
    list_filter = ('codigo',)  # Agregar filtro por código
    def get_queryset(self, request):
        # Forzar que el Admin use la base de datos SQLite
        return super().get_queryset(request).using('default')
admin.site.register(ActividadEconomica, ActividadEconomicaAdmin)

admin.site.register(Emisor_fe)
admin.site.register(representanteEmisor)

admin.site.register(Receptor_fe)

class Tipo_dtecaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')  # Agregar campo de búsqueda
    list_filter = ('codigo',)  # Agregar filtro por código
    def get_queryset(self, request):
        # Forzar que el Admin use la base de datos SQLite
        return super().get_queryset(request).using('default')
admin.site.register(Tipo_dte, Tipo_dtecaAdmin)

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class DepartamentocaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')  # Agregar campo de búsqueda
    list_filter = ('codigo',)  # Agregar filtro por código
    def get_queryset(self, request):
        # Forzar que el Admin use la base de datos SQLite
        return super().get_queryset(request).using('default')
admin.site.register(Departamento, DepartamentocaAdmin)

class MunicipiocaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')  # Agregar campo de búsqueda
    list_filter = ('codigo',)  # Agregar filtro por código
    def get_queryset(self, request):
        # Forzar que el Admin use la base de datos SQLite
        return super().get_queryset(request).using('default')
admin.site.register(Municipio, MunicipiocaAdmin)

class AmbientecaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')  # Agregar campo de búsqueda
    list_filter = ('codigo',)  # Agregar filtro por código
    def get_queryset(self, request):
        # Forzar que el Admin use la base de datos SQLite
        return super().get_queryset(request).using('default')
admin.site.register(Ambiente, AmbientecaAdmin)


@admin.register(Modelofacturacion)
class ModelofacturacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(TipoTransmision)
class TipoTransmisionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(TipoContingencia)
class TipoContingenciaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(TipoRetencionIVAMH)
class TipoRetencionIVAMHAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(TipoGeneracionDocumento)
class TipoGeneracionDocumentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(TiposEstablecimientos)
class TiposEstablecimientosAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(TiposServicio_Medico)
class TiposServicioMedicoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

"""@admin.register(TipoItem)
class TipoItemAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')"""

@admin.register(CondicionOperacion)
class CondicionOperacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(FormasPago)
class FormasPagoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(Plazo)
class PlazoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

    # Registro automático de modelos en el admin
for model in models:
    admin.site.register(model)
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

class Token_dataAdmin(admin.ModelAdmin):
    list_display = ('token', 'nit_empresa', 'created_at')
    search_fields = ('token', 'nit_empresa')
    #list_filter = ('created_at')

admin.site.register(Token_data, Token_dataAdmin)


