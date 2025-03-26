from django.urls import path

from FE.api_views import ActividadEconomicaCreateAPIView, ActividadEconomicaDeleteAPIView, ActividadEconomicaDetailAPIView, ActividadEconomicaListAPIView, ActividadEconomicaUpdateAPIView, AmbientesListAPIView, CondicionDeOperacionListAPIView, DepartamentosListAPIView, DescuentosAPIView, EmisorCreateAPIView, EnviarFacturaHaciendaAPIView, FacturaDetailAPIView, FacturaListAPIView, FirmarFacturaAPIView, FormasPagosListAPIView, GenerarFacturaAPIView, InvalidarDteUnificadoAPIView, AutenticacionAPIView, ModeloDeFacturacionListAPIView, MunicipioListAPIView, ObtenerReceptorAPIView, TipoDTEListAPIView, TipoDocIDReceptorListAPIView, TipoTransmisionListAPIView, TiposEstablecimientosListAPIView, TiposTributosListAPIView, TiposTributosSerializer, TributoByTipoListAPIView, TributoDetailsAPIView, autenticacion, EmisorListAPIView, productosListAPIView, recptorListAPIView, tipoGeneracionDocumentoListAPIView, GenerarDocumentoAjusteAPIView
from FE.serializers import TributosSerializer
from . import views

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
    path('api/factura_pdf/<int:pk>/', FacturaDetailAPIView.as_view(), name='factura_pdf_api'),
    
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
    path('api/descuentos/', DescuentosAPIView.as_view(), name='descuentos_api'),
    
    #URL FACTURAS
    path('api/facturas/', FacturaListAPIView.as_view(), name='factura_dte_api'),   
    
    #URL TIPO DE GENERACION DE FACTURAS
    path('api/tipo-generacion-facturas/', tipoGeneracionDocumentoListAPIView.as_view(), name='generacion_dte_api'), 
    
    #---------- URLS TRIBUTOS ----------#
    
    #URL TIPOS DE TRIBUTOS
    path('api/tipo-tributos/', TiposTributosListAPIView.as_view(), name='tipo_tributos_api'),
    
    #URL TRIBUTOS POR TIPO
    path('api/tributos/tipo/<int:tipo_valor>/', TributoByTipoListAPIView.as_view(), name='tributos_api'), 
    
    #TRIBUTOS POR ID    
    path('api/tributo/<int:pk>/', TributoDetailsAPIView.as_view(), name='tributo_api'), 
    
    
    #---------- URLS CONFIGURACION DE FACTURA ----------#
    #TIPO DE DOCUMENTO FACTURA
    path('api/tipo-dte/', TipoDTEListAPIView.as_view(), name='tipo_dte_list_api'),    
    
    #CONDICION DE OPERACION
    path('api/condicion-operacion/', CondicionDeOperacionListAPIView.as_view(), name='condicion_operacion_list_api'),
    
    #MODELO DE FACTURACION
    path('api/modelo-facturacion/', ModeloDeFacturacionListAPIView.as_view(), name='modelo_facturacion_list_api'),
    
    #CONTINGENCIA
    #path('api/contingencia_dte/<int:factura_id>/', ContingenciaDteAPIView.as_view(), name='contingencia_dte_api_view'),
    path('api/tipo-transmision/', TipoTransmisionListAPIView.as_view(), name='modelo_facturacion_list_api'),
    
    #FORMAS DE PAGO
    path('api/formas-pago/', FormasPagosListAPIView.as_view(), name='formas_pago_list_api'),

]
