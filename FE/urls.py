from django.urls import path
from . import views
from .views import (
    ActividadEconomicaDetailView,
    ActividadEconomicaCreateView, ActividadEconomicaUpdateView, ActividadEconomicaDeleteView,
    EmisorListView, EmisorDetailView, EmisorCreateView, EmisorUpdateView, EmisorDeleteView, 
    detalle_factura,
    enviar_factura_hacienda_view,
    enviar_factura_invalidacion_hacienda_view,
    firmar_factura_anulacion_view,
    firmar_factura_view,
    generar_factura_view,
    invalidacion_dte_view,
    obtener_numero_control_ajax,
    obtener_receptor,
    generar_documento_ajuste_view, 
    obtener_listado_productos_view
)


#renombrar el archivo
urlpatterns = [
    #urls para procesamiento de facturas
    path('generar/', generar_factura_view, name='generar_factura'),
    
    # URLS DTE AJUSTE
    path('generar_ajuste/', generar_documento_ajuste_view, name='generar_ajuste_factura'),

    #path('detalle/<int:factura_id>/', views.detalle_factura_view, name='detalle_factura'),
    path('listar_facturas/', views.factura_list, name='listar_facturas'),

    path('firmar/<int:factura_id>/', firmar_factura_view, name='firmar_factura'),
    path('enviar/<int:factura_id>/', enviar_factura_hacienda_view, name='enviar_factura_hacienda'),

    path('generarInv/<int:factura_id>/', invalidacion_dte_view, name='generar_inv_factura_hacienda'),
    path('firmarInv/<int:factura_id>/', firmar_factura_anulacion_view, name='firmar_factura_inv_hacienda'),
    path('invalidarDte/<int:factura_id>/', enviar_factura_invalidacion_hacienda_view, name='invalidar_factura_hacienda'),

    path('invalidar-dte/<int:factura_id>/', views.invalidar_dte_unificado_view, name='invalidar_dte_unificado'),
    path('invalidar-varias-dte/', views.invalidar_varias_dte_view, name='invalidar_varias_dte'),

    path('exportar-facturas/', views.export_facturas_excel, name='exportar_facturas_excel'),

    #path('factura/pdf/<int:factura_id>/', views.generar_factura_pdf, name='generar_factura_pdf'),
    #path('factura/pdf/<int:factura_id>/', views.generar_factura_pdf_2, name='generar_factura_pdf_2'),
    path("factura_pdf/<int:factura_id>/", detalle_factura, name="detalle_factura"),

    path('obtener-numero-control/', views.obtener_numero_control_ajax, name='obtener_numero_control_ajax'),
    path('obtener-descuento/', views.seleccion_descuento_ajax, name='obtener_descuento'),
    path('obtener-forma-pago/', views.agregar_formas_pago_ajax, name='agregar_formas_pago_ajax'),
    path('documento-relacionado/', views.obtener_factura_por_codigo, name='obtener_factura_por_codigo'),

    #urls para actividad economica
    path('actividades/', views.actividad_economica_list, name='actividad_economica_list'),
    path('actividad/<int:pk>/', ActividadEconomicaDetailView.as_view(), name='actividad_economica_detail'),
    path('actividad/new/', ActividadEconomicaCreateView.as_view(), name='actividad_economica_create'),
    path('actividad/<int:pk>/edit/', ActividadEconomicaUpdateView.as_view(), name='actividad_economica_update'),
    path('actividad/<int:pk>/delete/', ActividadEconomicaDeleteView.as_view(), name='actividad_economica_delete'),
    path('cargar-actividades/', views.cargar_actividades, name='cargar_actividades'),

    #url para emisor o empresa
    path('emisor/', EmisorListView.as_view(), name='emisor_list'),
    path('emisor/<int:pk>/', EmisorDetailView.as_view(), name='emisor_detail'),
    path('emisor/new/', EmisorCreateView.as_view(), name='emisor_create'),
    path('emisor/<int:pk>/edit/', EmisorUpdateView.as_view(), name='emisor_update'),
    path('emisor/<int:pk>/delete/', EmisorDeleteView.as_view(), name='emisor_delete'),
    
    #LISTADO DE PRODUCTOS
    path('obtener-listado-productos/', views.obtener_listado_productos_view, name='obtener_listado_productos_view'),
    
    #Contingencia
    path('listar_contingencias/', views.contingencia_list, name='listar_contingencias'),
    path('contingencia-dte/', views.contingencia_dte_unificado_view, name='contingencia_dte_unificado'),
    path('enviar-contingencias-dte/', views.contingencias_dte_view, name='contingencias_dte'),
    path('finalizar-contingencias/', views.finalizar_contigencia_view, name='finalizar_contigencia'),
    
    #Lotes
    path('lote-contingencia-dte/<int:contingencia_id>/', views.lote_contingencia_dte_view, name='lote_contingencia_dte'),
    path('enviar-lote-unificado/', views.envio_dte_unificado_view, name='envio_dte_unificado'),
    path('enviar-lotes/', views.lotes_dte_view, name='lotes_dte'),
]