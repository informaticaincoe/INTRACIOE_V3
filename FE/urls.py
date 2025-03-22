from django.urls import path

from FE.api_views import ActividadEconomicaCreateAPIView, ActividadEconomicaDeleteAPIView, ActividadEconomicaDetailAPIView, ActividadEconomicaListAPIView, ActividadEconomicaUpdateAPIView, AmbientesListAPIView, CondicionDeOperacionListAPIView, DepartamentosListAPIView, EmisorCreateAPIView, EnviarFacturaHaciendaAPIView, FacturasListAPIView, FirmarFacturaAPIView, GenerarFacturaAPIView, InvalidarDteUnificadoAPIView, AutenticacionAPIView, ModeloDeFacturacionListAPIView, MunicipioListAPIView, ObtenerReceptorAPIView, TipoDTEListAPIView, TipoDocIDReceptorListAPIView, TipoTransmisionListAPIView, TiposEstablecimientosListAPIView, TiposTributosListAPIView, TiposTributosSerializer, TributoListAPIView, autenticacion, EmisorListAPIView, productosListAPIView, recptorListAPIView, tipoGeneracionDocumentoListAPIView
from FE.serializers import TributosSerializer
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
    generar_documento_ajuste
)


#renombrar el archivo
urlpatterns = [
    # -------------------------------
    # Endpoints API REST
    # -------------------------------

    # Autenticación vía API
    path('api/auth/', AutenticacionAPIView.as_view(), name='api_auth'),

    # Autenticación vía formulario web
    path('api/autenticacion/', autenticacion, name='autenticacion'),

    path('api/invalidar_dte/<int:factura_id>/', InvalidarDteUnificadoAPIView.as_view(), name='api_invalidar_firmar_enviar'),
    path('api/factura/generar/', GenerarFacturaAPIView.as_view(), name='generar_factura_api'),
    path('api/factura/firmar/<int:factura_id>/', FirmarFacturaAPIView.as_view(), name='firmar_factura_api'),
    path('api/factura/enviar_hacienda/<int:factura_id>/', EnviarFacturaHaciendaAPIView.as_view(), name='enviar_factura_hacienda_api'),
    path('api/factura_ajuste/generar/', GenerarDocumentoAjusteAPIView.as_view(), name='generar_factura_ajuste_api'), #Nota de credito y nota de debito
    
    # URLS DE API ACTIVIDAD ECONOMICA 
    path('api/actividad/', ActividadEconomicaListAPIView.as_view(), name='actividad_list_api'),

    path('api/actividad/<int:pk>/', ActividadEconomicaDetailAPIView.as_view(), name='actividad_detail_api'),
    path('api/actividad/crear/', ActividadEconomicaCreateAPIView.as_view(), name='actividad_create_api'),
    path('api/actividad/actualizar/<int:pk>/', ActividadEconomicaUpdateAPIView.as_view(), name='actividad_update_api'),
    path('api/actividad/eliminar/<int:pk>/', ActividadEconomicaDeleteAPIView.as_view(), name='actividad_delete_api'),
    
    #URLS API EMISOR
    path('api/emisor/', EmisorListAPIView.as_view(), name='emisor_list_api'),
    path('api/emisor/crear/', EmisorCreateAPIView.as_view(), name='emisor_create_api'),
    
    #URLS TIPO DOCUMENTO
    path('api/tipo-id-receptor/', TipoDocIDReceptorListAPIView.as_view(), name='tipo_doc_id_receptor_list_api'),
    
    #URLS AMBIENTE
    path('api/ambientes/', AmbientesListAPIView.as_view(), name='ambientes_list_api'),
    
    #URLS TIPOS ESTABLECIMIENTO
    path('api/tipo-establecimiento/', TiposEstablecimientosListAPIView.as_view(), name='establecimientos_list_api'),
    
    
    #URLS DEPARTAMENTOS
    path('api/departamentos/', DepartamentosListAPIView.as_view(), name='departamentos_list_api'),
    
    #URLS MUNICIPIOS SEGUN DEPARTAMENTO
    path('api/municipio/<int:pk>/', MunicipioListAPIView.as_view(), name='municipio_list_api'), 
    
    #URLS RECEPTOR
    path('api/receptor/', recptorListAPIView.as_view(), name='receptor_list_api'),
         
    
    #URL PRODUCTOS
    path('api/productos/', productosListAPIView.as_view(), name='tipo_dte_api'),   
    
    #URL FACTURAS
    path('api/facturas/', FacturasListAPIView.as_view(), name='factura_dte_api'),   
    
    #URL TIPO DE GENERACION DE FACTURAS
    path('api/tipo-generacion-facturas/', tipoGeneracionDocumentoListAPIView.as_view(), name='generacion_dte_api'), 
    
    #---------- URLS TRIBUTOS ----------#
    
    #URL TIPOS DE TRIBUTOS
    path('api/tipo-tributos/', TiposTributosListAPIView.as_view(), name='tipo_tributos_api'),
    
    #URL TIPOS DE TRIBUTOS
    path('api/tributos/<int:tipo_valor>/', TributoListAPIView.as_view(), name='tributos_api'), 
    
    #---------- URLS CONFIGURACION DE FACTURA ----------#
    #TIPO DE DOCUMENTO FACTURA
    path('api/tipo-dte/', TipoDTEListAPIView.as_view(), name='tipo_dte_list_api'),    
    
    #CONDICION DE OPERACION
    path('api/condicion-operacion/', CondicionDeOperacionListAPIView.as_view(), name='condicion_operacion_list_api'),
    
    #MODELO DE FACTURACION
    path('api/modelo-facturacion/', ModeloDeFacturacionListAPIView.as_view(), name='modelo_facturacion_list_api'),
    
    path('api/tipo-transmision/', TipoTransmisionListAPIView.as_view(), name='modelo_facturacion_list_api'),
    
    
    ################################################################################################################################################
    ################################################################################################################################################

    #urls para procesamiento de facturas
    path('generar/', generar_factura_view, name='generar_factura'),
    
    # URLS DTE AJUSTE
    path('factura/generar_ajuste/', generar_documento_ajuste, name='generar_ajuste_factura'),

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
]
