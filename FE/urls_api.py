
from django.urls import path
from FE.api_views import (
    ContingenciaDteAPIView, ContingenciaListAPIView, EmisorCreateAPIView, EmisorUpdateAPIView, EnviarFacturaHaciendaAPIView, FacturaDetailAPIView, FacturaListAPIView, FacturaPorCodigoGeneracionAPIView, FirmarFacturaAPIView, 
    GenerarFacturaAPIView, InvalidarDteUnificadoAPIView, AutenticacionAPIView, LoteContingenciaDteAPIView, MunicipioByDepartamentoAPIView, ObtenerReceptorAPIView, autenticacion, EmisorListAPIView, receptorCreateAPIView, receptorDeleteAPIView, receptorDetailAPIView, 
    receptorListAPIView, receptorUpdateAPIView, GenerarDocumentoAjusteAPIView,

    # ACTIVIDAD ECONOMICA
    ActividadEconomicaListAPIView, ActividadEconomicaCreateAPIView, ActividadEconomicaRetrieveAPIView,
    ActividadEconomicaUpdateAPIView, ActividadEconomicaDestroyAPIView,
    # AMBIENTE
    AmbienteListAPIView, AmbienteCreateAPIView, AmbienteRetrieveAPIView, AmbienteUpdateAPIView, AmbienteDestroyAPIView,
    # MODELO FACTURACION
    ModelofacturacionListAPIView, ModelofacturacionCreateAPIView, ModelofacturacionRetrieveAPIView,
    ModelofacturacionUpdateAPIView, ModelofacturacionDestroyAPIView,
    # TIPO TRANSMISION
    TipoTransmisionListAPIView, TipoTransmisionCreateAPIView, TipoTransmisionRetrieveAPIView,
    TipoTransmisionUpdateAPIView, TipoTransmisionDestroyAPIView,
    # TIPO CONTINGENCIA
    TipoContingenciaListAPIView, TipoContingenciaCreateAPIView, TipoContingenciaRetrieveAPIView,
    TipoContingenciaUpdateAPIView, TipoContingenciaDestroyAPIView,
    # TIPO RETENCION IVA MH
    TipoRetencionIVAMHListAPIView, TipoRetencionIVAMHCreateAPIView, TipoRetencionIVAMHRetrieveAPIView,
    TipoRetencionIVAMHUpdateAPIView, TipoRetencionIVAMHDestroyAPIView,
    # TIPO GENERACION DOCUMENTO
    TipoGeneracionDocumentoListAPIView, TipoGeneracionDocumentoCreateAPIView, TipoGeneracionDocumentoRetrieveAPIView,
    TipoGeneracionDocumentoUpdateAPIView, TipoGeneracionDocumentoDestroyAPIView,
    # TIPOS ESTABLECIMIENTOS
    TiposEstablecimientosListAPIView, TiposEstablecimientosCreateAPIView, TiposEstablecimientosRetrieveAPIView,
    TiposEstablecimientosUpdateAPIView, TiposEstablecimientosDestroyAPIView,
    # TIPOS SERVICIO MEDICO
    TiposServicio_MedicoListAPIView, TiposServicio_MedicoCreateAPIView, TiposServicio_MedicoRetrieveAPIView,
    TiposServicio_MedicoUpdateAPIView, TiposServicio_MedicoDestroyAPIView,
    # TIPO_DTE
    Tipo_dteListAPIView, Tipo_dteCreateAPIView, Tipo_dteRetrieveAPIView,
    Tipo_dteUpdateAPIView, Tipo_dteDestroyAPIView,
    # OTROS DOCUMENTOS ASOCIADO
    OtrosDicumentosAsociadoListAPIView, OtrosDicumentosAsociadoCreateAPIView, OtrosDicumentosAsociadoRetrieveAPIView,
    OtrosDicumentosAsociadoUpdateAPIView, OtrosDicumentosAsociadoDestroyAPIView,
    # TIPOS DOC ID RECEPTOR
    TiposDocIDReceptorListAPIView, TiposDocIDReceptorCreateAPIView, TiposDocIDReceptorRetrieveAPIView,
    TiposDocIDReceptorUpdateAPIView, TiposDocIDReceptorDestroyAPIView,
    # PAIS
    PaisListAPIView, PaisCreateAPIView, PaisRetrieveAPIView, PaisUpdateAPIView, PaisDestroyAPIView,
    # DEPARTAMENTO
    DepartamentoListAPIView, DepartamentoCreateAPIView, DepartamentoRetrieveAPIView, DepartamentoUpdateAPIView, DepartamentoDestroyAPIView,
    # MUNICIPIO
    MunicipioListAPIView, MunicipioCreateAPIView, MunicipioRetrieveAPIView, MunicipioUpdateAPIView, MunicipioDestroyAPIView,
    # CONDICION OPERACION
    CondicionOperacionListAPIView, CondicionOperacionCreateAPIView, CondicionOperacionRetrieveAPIView,
    CondicionOperacionUpdateAPIView, CondicionOperacionDestroyAPIView,
    # FORMAS PAGO
    FormasPagoListAPIView, FormasPagoCreateAPIView, FormasPagoRetrieveAPIView, FormasPagoUpdateAPIView, FormasPagoDestroyAPIView,
    # PLAZO
    PlazoListAPIView, PlazoCreateAPIView, PlazoRetrieveAPIView, PlazoUpdateAPIView, PlazoDestroyAPIView,
    # TIPO DOC CONTINGENCIA
    TipoDocContingenciaListAPIView, TipoDocContingenciaCreateAPIView, TipoDocContingenciaRetrieveAPIView,
    TipoDocContingenciaUpdateAPIView, TipoDocContingenciaDestroyAPIView,
    # TIPO INVALIDACION
    TipoInvalidacionListAPIView, TipoInvalidacionCreateAPIView, TipoInvalidacionRetrieveAPIView,
    TipoInvalidacionUpdateAPIView, TipoInvalidacionDestroyAPIView,
    # TIPO DONACION
    TipoDonacionListAPIView, TipoDonacionCreateAPIView, TipoDonacionRetrieveAPIView,
    TipoDonacionUpdateAPIView, TipoDonacionDestroyAPIView,
    # TIPO PERSONA
    TipoPersonaListAPIView, TipoPersonaCreateAPIView, TipoPersonaRetrieveAPIView,
    TipoPersonaUpdateAPIView, TipoPersonaDestroyAPIView,
    # TIPO TRANSPORTE
    TipoTransporteListAPIView, TipoTransporteCreateAPIView, TipoTransporteRetrieveAPIView,
    TipoTransporteUpdateAPIView, TipoTransporteDestroyAPIView,
    # INCOTERMS
    INCOTERMSListAPIView, INCOTERMSCreateAPIView, INCOTERMSRetrieveAPIView,
    INCOTERMSUpdateAPIView, INCOTERMSDestroyAPIView,
    # TIPO DOMICILIO FISCAL
    TipoDomicilioFiscalListAPIView, TipoDomicilioFiscalCreateAPIView, TipoDomicilioFiscalRetrieveAPIView,
    TipoDomicilioFiscalUpdateAPIView, TipoDomicilioFiscalDestroyAPIView,
    # TIPO MONEDA
    TipoMonedaListAPIView, TipoMonedaCreateAPIView, TipoMonedaRetrieveAPIView,
    TipoMonedaUpdateAPIView, TipoMonedaDestroyAPIView,
    # DESCUENTO
    DescuentoListAPIView, DescuentoCreateAPIView, DescuentoRetrieveAPIView,
    DescuentoUpdateAPIView, DescuentoDestroyAPIView

    )
from . import views

#renombrar el archivo
urlpatterns = [

    # Autenticación vía API
    path('api/auth/', AutenticacionAPIView.as_view(), name='api_auth'),

    # Autenticación vía formulario web
    path('api/autenticacion/', autenticacion, name='autenticacion'),

    ##################################################################
    # URLS CATALOGO
    ##################################################################

    # ACTIVIDAD ECONOMICA
    path('api/actividad/', ActividadEconomicaListAPIView.as_view(), name='actividad_list_api'),
    path('api/actividad/crear/', ActividadEconomicaCreateAPIView.as_view(), name='actividad_create_api'),
    path('api/actividad/<int:pk>/', ActividadEconomicaRetrieveAPIView.as_view(), name='actividad_detail_api'),
    path('api/actividad/actualizar/<int:pk>/', ActividadEconomicaUpdateAPIView.as_view(), name='actividad_update_api'),
    path('api/actividad/eliminar/<int:pk>/', ActividadEconomicaDestroyAPIView.as_view(), name='actividad_delete_api'),
    
    # AMBIENTE
    path('api/ambientes/', AmbienteListAPIView.as_view(), name='ambientes_list_api'),
    path('api/ambiente/crear/', AmbienteCreateAPIView.as_view(), name='ambiente-create'),
    path('api/ambiente/<int:pk>/', AmbienteRetrieveAPIView.as_view(), name='ambiente-detail'),
    path('api/ambiente/<int:pk>/editar/', AmbienteUpdateAPIView.as_view(), name='ambiente-update'),
    path('api/ambiente/<int:pk>/eliminar/', AmbienteDestroyAPIView.as_view(), name='ambiente-destroy'),
    
    # MODELO FACTURACION
    path('api/modelo-facturacion/', ModelofacturacionListAPIView.as_view(), name='modelo_facturacion_list_api'),
    path('api/modelo-facturacion/crear/', ModelofacturacionCreateAPIView.as_view(), name='modelo-facturacion-create'),
    path('api/modelo-facturacion/<int:pk>/', ModelofacturacionRetrieveAPIView.as_view(), name='modelo-facturacion-detail'),
    path('api/modelo-facturacion/<int:pk>/editar/', ModelofacturacionUpdateAPIView.as_view(), name='modelo-facturacion-update'),
    path('api/modelo-facturacion/<int:pk>/eliminar/', ModelofacturacionDestroyAPIView.as_view(), name='modelo-facturacion-destroy'),
    
    # TIPO TRANSMISION
    path('api/tipo-transmision/', TipoTransmisionListAPIView.as_view(), name='modelo_facturacion_list_api'),
    path('api/tipo-transmision/crear/', TipoTransmisionCreateAPIView.as_view(), name='tipo-transmision-create'),
    path('api/tipo-transmision/<int:pk>/', TipoTransmisionRetrieveAPIView.as_view(), name='tipo-transmision-detail'),
    path('api/tipo-transmision/<int:pk>/editar/', TipoTransmisionUpdateAPIView.as_view(), name='tipo-transmision-update'),
    path('api/tipo-transmision/<int:pk>/eliminar/', TipoTransmisionDestroyAPIView.as_view(), name='tipo-transmision-destroy'),
    
    # TIPO CONTINGENCIA
    path('api/tipo-contingencia/', TipoContingenciaListAPIView.as_view(), name='tipo-contingencia-list'),
    path('api/tipo-contingencia/crear/', TipoContingenciaCreateAPIView.as_view(), name='tipo-contingencia-create'),
    path('api/tipo-contingencia/<int:pk>/', TipoContingenciaRetrieveAPIView.as_view(), name='tipo-contingencia-detail'),
    path('api/tipo-contingencia/<int:pk>/editar/', TipoContingenciaUpdateAPIView.as_view(), name='tipo-contingencia-update'),
    path('api/tipo-contingencia/<int:pk>/eliminar/', TipoContingenciaDestroyAPIView.as_view(), name='tipo-contingencia-destroy'),
    
    # TIPO RETENCION IVA MH
    path('api/tipo-retencion-iva-mh/', TipoRetencionIVAMHListAPIView.as_view(), name='tipo-retencion-iva-mh-list'),
    path('api/tipo-retencion-iva-mh/crear/', TipoRetencionIVAMHCreateAPIView.as_view(), name='tipo-retencion-iva-mh-create'),
    path('api/tipo-retencion-iva-mh/<int:pk>/', TipoRetencionIVAMHRetrieveAPIView.as_view(), name='tipo-retencion-iva-mh-detail'),
    path('api/tipo-retencion-iva-mh/<int:pk>/editar/', TipoRetencionIVAMHUpdateAPIView.as_view(), name='tipo-retencion-iva-mh-update'),
    path('api/tipo-retencion-iva-mh/<int:pk>/eliminar/', TipoRetencionIVAMHDestroyAPIView.as_view(), name='tipo-retencion-iva-mh-destroy'),
    
    # TIPO GENERACION DOCUMENTO
    path('api/tipo-generacion-facturas/', TipoGeneracionDocumentoListAPIView.as_view(), name='generacion_dte_api'), 
    path('api/tipo-generacion-documento/crear/', TipoGeneracionDocumentoCreateAPIView.as_view(), name='tipo-generacion-documento-create'),
    path('api/tipo-generacion-documento/<int:pk>/', TipoGeneracionDocumentoRetrieveAPIView.as_view(), name='tipo-generacion-documento-detail'),
    path('api/tipo-generacion-documento/<int:pk>/editar/', TipoGeneracionDocumentoUpdateAPIView.as_view(), name='tipo-generacion-documento-update'),
    path('api/tipo-generacion-documento/<int:pk>/eliminar/', TipoGeneracionDocumentoDestroyAPIView.as_view(), name='tipo-generacion-documento-destroy'),
    
    # TIPOS ESTABLECIMIENTOS
    path('api/tipo-establecimiento/', TiposEstablecimientosListAPIView.as_view(), name='establecimientos_list_api'),
    path('api/tipos-establecimientos/crear/', TiposEstablecimientosCreateAPIView.as_view(), name='tipos-establecimientos-create'),
    path('api/tipos-establecimientos/<int:pk>/', TiposEstablecimientosRetrieveAPIView.as_view(), name='tipos-establecimientos-detail'),
    path('api/tipos-establecimientos/<int:pk>/editar/', TiposEstablecimientosUpdateAPIView.as_view(), name='tipos-establecimientos-update'),
    path('api/tipos-establecimientos/<int:pk>/eliminar/', TiposEstablecimientosDestroyAPIView.as_view(), name='tipos-establecimientos-destroy'),
    
    # TIPOS SERVICIO MEDICO
    path('api/tipos-servicio-medico/', TiposServicio_MedicoListAPIView.as_view(), name='tipos-servicio-medico-list'),
    path('api/tipos-servicio-medico/crear/', TiposServicio_MedicoCreateAPIView.as_view(), name='tipos-servicio-medico-create'),
    path('api/tipos-servicio-medico/<int:pk>/', TiposServicio_MedicoRetrieveAPIView.as_view(), name='tipos-servicio-medico-detail'),
    path('api/tipos-servicio-medico/<int:pk>/editar/', TiposServicio_MedicoUpdateAPIView.as_view(), name='tipos-servicio-medico-update'),
    path('api/tipos-servicio-medico/<int:pk>/eliminar/', TiposServicio_MedicoDestroyAPIView.as_view(), name='tipos-servicio-medico-destroy'),
    
    # TIPO_DTE
    path('api/tipo-dte/', Tipo_dteListAPIView.as_view(), name='tipo_dte_list_api'),
    path('api/tipo-dte/crear/', Tipo_dteCreateAPIView.as_view(), name='tipo-dte-create'),
    path('api/tipo-dte/<str:codigo>/', Tipo_dteRetrieveAPIView.as_view(), name='tipo_dte_detail_api'),
    path('api/tipo-dte/<int:pk>/editar/', Tipo_dteUpdateAPIView.as_view(), name='tipo-dte-update'),
    path('api/tipo-dte/<int:pk>/eliminar/', Tipo_dteDestroyAPIView.as_view(), name='tipo-dte-destroy'),
    
    # OTROS DOCUMENTOS ASOCIADO
    path('api/otros-documentos-asociado/', OtrosDicumentosAsociadoListAPIView.as_view(), name='otros-documentos-asociado-list'),
    path('api/otros-documentos-asociado/crear/', OtrosDicumentosAsociadoCreateAPIView.as_view(), name='otros-documentos-asociado-create'),
    path('api/otros-documentos-asociado/<int:pk>/', OtrosDicumentosAsociadoRetrieveAPIView.as_view(), name='otros-documentos-asociado-detail'),
    path('api/otros-documentos-asociado/<int:pk>/editar/', OtrosDicumentosAsociadoUpdateAPIView.as_view(), name='otros-documentos-asociado-update'),
    path('api/otros-documentos-asociado/<int:pk>/eliminar/', OtrosDicumentosAsociadoDestroyAPIView.as_view(), name='otros-documentos-asociado-destroy'),
    
    # TIPOS DOC ID RECEPTOR
    path('api/tipo-id-receptor/', TiposDocIDReceptorListAPIView.as_view(), name='tipo_doc_id_receptor_list_api'),
    path('api/tipos-doc-id-receptor/crear/', TiposDocIDReceptorCreateAPIView.as_view(), name='tipos-doc-id-receptor-create'),
    path('api/tipo-id-receptor/<str:codigo>/', TiposDocIDReceptorRetrieveAPIView.as_view(), name='tipo_doc_id_receptor_datail_api'),
    path('api/tipos-doc-id-receptor/<int:pk>/editar/', TiposDocIDReceptorUpdateAPIView.as_view(), name='tipos-doc-id-receptor-update'),
    path('api/tipos-doc-id-receptor/<int:pk>/eliminar/', TiposDocIDReceptorDestroyAPIView.as_view(), name='tipos-doc-id-receptor-destroy'),
    
    # PAIS
    path('api/pais/', PaisListAPIView.as_view(), name='pais-list'),
    path('api/pais/crear/', PaisCreateAPIView.as_view(), name='pais-create'),
    path('api/pais/<int:pk>/', PaisRetrieveAPIView.as_view(), name='pais-detail'),
    path('api/pais/<int:pk>/editar/', PaisUpdateAPIView.as_view(), name='pais-update'),
    path('api/pais/<int:pk>/eliminar/', PaisDestroyAPIView.as_view(), name='pais-destroy'),
    
    # DEPARTAMENTO
    path('api/departamentos/', DepartamentoListAPIView.as_view(), name='departamentos_list_api'),
    path('api/departamento/crear/', DepartamentoCreateAPIView.as_view(), name='departamento-create'),
    path('api/departamento/<int:pk>/', DepartamentoRetrieveAPIView.as_view(), name='departamento-detail'),
    path('api/departamento/<int:pk>/editar/', DepartamentoUpdateAPIView.as_view(), name='departamento-update'),
    path('api/departamento/<int:pk>/eliminar/', DepartamentoDestroyAPIView.as_view(), name='departamento-destroy'),
    
    # MUNICIPIO
    path('api/municipio/<int:pk>/', MunicipioListAPIView.as_view(), name='municipio_list_api'),
    path('api/municipio/crear/', MunicipioCreateAPIView.as_view(), name='municipio-create'),
    path('api/municipio-by-id/<int:pk>/', MunicipioRetrieveAPIView.as_view(), name='municipio_detail_api'),
     path('api/municipios/departamento/<int:departamento_id>/', MunicipioByDepartamentoAPIView.as_view(), name='municipios_by_departamento'), 
    path('api/municipio/<int:pk>/editar/', MunicipioUpdateAPIView.as_view(), name='municipio-update'),
    path('api/municipio/<int:pk>/eliminar/', MunicipioDestroyAPIView.as_view(), name='municipio-destroy'),
    
    # CONDICION OPERACION
    path('api/condicion-operacion/', CondicionOperacionListAPIView.as_view(), name='condicion_operacion_list_api'),
    path('api/condicion-operacion/crear/', CondicionOperacionCreateAPIView.as_view(), name='condicion-operacion-create'),
    path('api/condicion-operacion/<str:codigo>/', CondicionOperacionRetrieveAPIView.as_view(), name='condicion_operacion_list_api'),
    path('api/condicion-operacion/<int:pk>/editar/', CondicionOperacionUpdateAPIView.as_view(), name='condicion-operacion-update'),
    path('api/condicion-operacion/<int:pk>/eliminar/', CondicionOperacionDestroyAPIView.as_view(), name='condicion-operacion-destroy'),
    
    # FORMAS PAGO
    path('api/formas-pago/', FormasPagoListAPIView.as_view(), name='formas_pago_list_api'),
    path('api/formas-pago/crear/', FormasPagoCreateAPIView.as_view(), name='formas-pago-create'),
    path('api/formas-pago/<int:pk>/', FormasPagoRetrieveAPIView.as_view(), name='formas-pago-detail'),
    path('api/formas-pago/<int:pk>/editar/', FormasPagoUpdateAPIView.as_view(), name='formas-pago-update'),
    path('api/formas-pago/<int:pk>/eliminar/', FormasPagoDestroyAPIView.as_view(), name='formas-pago-destroy'),
    
    # PLAZO
    path('api/plazo/', PlazoListAPIView.as_view(), name='plazo-list'),
    path('api/plazo/crear/', PlazoCreateAPIView.as_view(), name='plazo-create'),
    path('api/plazo/<int:pk>/', PlazoRetrieveAPIView.as_view(), name='plazo-detail'),
    path('api/plazo/<int:pk>/editar/', PlazoUpdateAPIView.as_view(), name='plazo-update'),
    path('api/plazo/<int:pk>/eliminar/', PlazoDestroyAPIView.as_view(), name='plazo-destroy'),
    
    # TIPO DOC CONTINGENCIA
    path('api/tipo-doc-contingencia/', TipoDocContingenciaListAPIView.as_view(), name='tipo-doc-contingencia-list'),
    path('api/tipo-doc-contingencia/crear/', TipoDocContingenciaCreateAPIView.as_view(), name='tipo-doc-contingencia-create'),
    path('api/tipo-doc-contingencia/<int:pk>/', TipoDocContingenciaRetrieveAPIView.as_view(), name='tipo-doc-contingencia-detail'),
    path('api/tipo-doc-contingencia/<int:pk>/editar/', TipoDocContingenciaUpdateAPIView.as_view(), name='tipo-doc-contingencia-update'),
    path('api/tipo-doc-contingencia/<int:pk>/eliminar/', TipoDocContingenciaDestroyAPIView.as_view(), name='tipo-doc-contingencia-destroy'),
    
    # TIPO INVALIDACION
    path('api/tipo-invalidacion/', TipoInvalidacionListAPIView.as_view(), name='tipo-invalidacion-list'),
    path('api/tipo-invalidacion/crear/', TipoInvalidacionCreateAPIView.as_view(), name='tipo-invalidacion-create'),
    path('api/tipo-invalidacion/<int:pk>/', TipoInvalidacionRetrieveAPIView.as_view(), name='tipo-invalidacion-detail'),
    path('api/tipo-invalidacion/<int:pk>/editar/', TipoInvalidacionUpdateAPIView.as_view(), name='tipo-invalidacion-update'),
    path('api/tipo-invalidacion/<int:pk>/eliminar/', TipoInvalidacionDestroyAPIView.as_view(), name='tipo-invalidacion-destroy'),
    
    # TIPO DONACION
    path('api/tipo-donacion/', TipoDonacionListAPIView.as_view(), name='tipo-donacion-list'),
    path('api/tipo-donacion/crear/', TipoDonacionCreateAPIView.as_view(), name='tipo-donacion-create'),
    path('api/tipo-donacion/<int:pk>/', TipoDonacionRetrieveAPIView.as_view(), name='tipo-donacion-detail'),
    path('api/tipo-donacion/<int:pk>/editar/', TipoDonacionUpdateAPIView.as_view(), name='tipo-donacion-update'),
    path('api/tipo-donacion/<int:pk>/eliminar/', TipoDonacionDestroyAPIView.as_view(), name='tipo-donacion-destroy'),
    
    # TIPO PERSONA
    path('api/tipo-persona/', TipoPersonaListAPIView.as_view(), name='tipo-persona-list'),
    path('api/tipo-persona/crear/', TipoPersonaCreateAPIView.as_view(), name='tipo-persona-create'),
    path('api/tipo-persona/<int:pk>/', TipoPersonaRetrieveAPIView.as_view(), name='tipo-persona-detail'),
    path('api/tipo-persona/<int:pk>/editar/', TipoPersonaUpdateAPIView.as_view(), name='tipo-persona-update'),
    path('api/tipo-persona/<int:pk>/eliminar/', TipoPersonaDestroyAPIView.as_view(), name='tipo-persona-destroy'),
    
    # TIPO TRANSPORTE
    path('api/tipo-transporte/', TipoTransporteListAPIView.as_view(), name='tipo-transporte-list'),
    path('api/tipo-transporte/crear/', TipoTransporteCreateAPIView.as_view(), name='tipo-transporte-create'),
    path('api/tipo-transporte/<int:pk>/', TipoTransporteRetrieveAPIView.as_view(), name='tipo-transporte-detail'),
    path('api/tipo-transporte/<int:pk>/editar/', TipoTransporteUpdateAPIView.as_view(), name='tipo-transporte-update'),
    path('api/tipo-transporte/<int:pk>/eliminar/', TipoTransporteDestroyAPIView.as_view(), name='tipo-transporte-destroy'),
    
    # INCOTERMS
    path('api/incoterms/', INCOTERMSListAPIView.as_view(), name='incoterms-list'),
    path('api/incoterms/crear/', INCOTERMSCreateAPIView.as_view(), name='incoterms-create'),
    path('api/incoterms/<int:pk>/', INCOTERMSRetrieveAPIView.as_view(), name='incoterms-detail'),
    path('api/incoterms/<int:pk>/editar/', INCOTERMSUpdateAPIView.as_view(), name='incoterms-update'),
    path('api/incoterms/<int:pk>/eliminar/', INCOTERMSDestroyAPIView.as_view(), name='incoterms-destroy'),
    
    # TIPO DOMICILIO FISCAL
    path('api/tipo-domicilio-fiscal/', TipoDomicilioFiscalListAPIView.as_view(), name='tipo-domicilio-fiscal-list'),
    path('api/tipo-domicilio-fiscal/crear/', TipoDomicilioFiscalCreateAPIView.as_view(), name='tipo-domicilio-fiscal-create'),
    path('api/tipo-domicilio-fiscal/<int:pk>/', TipoDomicilioFiscalRetrieveAPIView.as_view(), name='tipo-domicilio-fiscal-detail'),
    path('api/tipo-domicilio-fiscal/<int:pk>/editar/', TipoDomicilioFiscalUpdateAPIView.as_view(), name='tipo-domicilio-fiscal-update'),
    path('api/tipo-domicilio-fiscal/<int:pk>/eliminar/', TipoDomicilioFiscalDestroyAPIView.as_view(), name='tipo-domicilio-fiscal-destroy'),
    
    # TIPO MONEDA
    path('api/tipo-moneda/', TipoMonedaListAPIView.as_view(), name='tipo-moneda-list'),
    path('api/tipo-moneda/crear/', TipoMonedaCreateAPIView.as_view(), name='tipo-moneda-create'),
    path('api/tipo-moneda/<int:pk>/', TipoMonedaRetrieveAPIView.as_view(), name='tipo-moneda-detail'),
    path('api/tipo-moneda/<int:pk>/editar/', TipoMonedaUpdateAPIView.as_view(), name='tipo-moneda-update'),
    path('api/tipo-moneda/<int:pk>/eliminar/', TipoMonedaDestroyAPIView.as_view(), name='tipo-moneda-destroy'),
    
    # DESCUENTO
    path('api/descuento/', DescuentoListAPIView.as_view(), name='descuentos_api'),
    path('api/descuento/crear/', DescuentoCreateAPIView.as_view(), name='descuento-create'),
    path('api/descuento/<int:pk>/', DescuentoRetrieveAPIView.as_view(), name='descuento-detail'),
    path('api/descuento/<int:pk>/editar/', DescuentoUpdateAPIView.as_view(), name='descuento-update'),
    path('api/descuento/<int:pk>/eliminar/', DescuentoDestroyAPIView.as_view(), name='descuento-destroy'),

    ##################################################################
    # FIN URLS CATALOGO
    ##################################################################

    #-----------FACTURA -----------#
    path('api/facturas/', FacturaListAPIView.as_view(), name='api_factura_list'),
    path("api/factura-por-codigo/", FacturaPorCodigoGeneracionAPIView.as_view(), name="factura_por_codigo"),
    path('api/invalidar_dte/<int:factura_id>/', InvalidarDteUnificadoAPIView.as_view(), name='api_invalidar_firmar_enviar'),
    path('api/factura/generar/', GenerarFacturaAPIView.as_view(), name='generar_factura_api'),
    path('api/factura_pdf/<int:pk>/', FacturaDetailAPIView.as_view(), name='factura_pdf_api'),
    path('api/factura/firmar/<int:factura_id>/', FirmarFacturaAPIView.as_view(), name='firmar_factura_api'),
    path('api/factura/enviar_hacienda/<int:factura_id>/', EnviarFacturaHaciendaAPIView.as_view(), name='enviar_factura_hacienda_api'),
    path('api/factura_ajuste/generar/', GenerarDocumentoAjusteAPIView.as_view(), name='generar_factura_ajuste_api'), #Nota de credito y nota de debito
    # path('api/facturas/totales-por-tipo/', TotalesPorTipoDTE.as_view(), name='totales-por-tipo'),
    # path('api/facturas/totales-ventas/', TotalVentasAPIView.as_view(), name='total-ventas'),
    # path('api/facturas/clientes/', TopClientes.as_view(), name='Top-clientes'),
    # path('api/facturas/productos/', TopProductosAPIView.as_view(), name='Top-productos'),

    #----------- EMISOR / RECEPTOR -----------#
    path('api/emisor/', EmisorListAPIView.as_view(), name='emisor_list_api'),
    path('api/emisor/editar/<int:pk>/', EmisorUpdateAPIView.as_view(), name='emisor_list_api'),
    path('api/emisor/crear/', EmisorCreateAPIView.as_view(), name='emisor_create_api'),

    #Obtener todos los receptores
    path('api/receptor/', receptorListAPIView.as_view(), name='receptor_list_api'), 
    path('api/receptor/<int:pk>/', receptorDetailAPIView.as_view(), name='receptor_detail_api'), 
    path('api/receptor/crear/', receptorCreateAPIView.as_view(), name='receptor_list_api'), 
    path('api/receptor/actualizar/<int:pk>/', receptorUpdateAPIView.as_view(), name='receptor_list_api'), 
    path('api/receptor/eliminar/<int:pk>/', receptorDeleteAPIView.as_view(), name='receptor_list_api'), 


    ##################################################################
    # URLS CONTINGENCIA
    ##################################################################

    path('api/contingencia/', ContingenciaListAPIView.as_view(), name='contingencia-list'),
    path('api/contingencia/<int:contingencia_id>/generar/', ContingenciaDteAPIView.as_view(), name='contingencia-dte-generate'),
    path('api/contingencia/<int:contingencia_id>/generar/', ContingenciaDteAPIView.as_view(), name='contingencia-dte-generate'),
    path(
        'api/contingencia/<int:tipo_contingencia_id>/lote/<int:factura_id>/',
        LoteContingenciaDteAPIView.as_view(),
        name='lote-contingencia-dte'
    ),



]
