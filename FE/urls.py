from django.urls import path
from . import views
from . import views_ventas
from .views import (
    ActividadEconomicaDetailView,
    ActividadEconomicaCreateView, ActividadEconomicaUpdateView, ActividadEconomicaDeleteView,
    detalle_factura,
    enviar_factura_hacienda_view,
    enviar_factura_invalidacion_hacienda_view,
    factura_termica,
    firmar_factura_anulacion_view,
    firmar_factura_view,
    generar_factura_view,
    invalidacion_dte_view,
    obtener_numero_control_ajax,
    obtener_receptor,
    generar_documento_ajuste_view, 
    obtener_listado_productos_view,
    select_tipo_facturas_mes_home,
    listar_documentos_pendientes
    #generar_factura_exportacion_view
)

#renombrar el archivo
urlpatterns = [
    # url para obtener token de hacienda
    path("hacienda/token/", views.obtener_token_view, name="obtener_token_hacienda"),

    path("tipo-dte/nuevo/", views.crear_tipo_dte, name="crear_tipo_dte"),
    
    # Homes de facturación:
    path('fe/facturacion/generar/', views.facturacion_generar_home, name='facturacion_generar_home'),
    path('fe/facturacion/correcciones/', views.facturacion_correcciones_home, name='facturacion_correcciones_home'),

    #urls para procesamiento de facturas
    path('generar/', generar_factura_view, name='generar_factura'),
    #path('generar_exportacion/', generar_factura_exportacion_view, name='generar_factura_exportacion'),
    
    # URLS DTE AJUSTE
    path('generar_ajuste/', generar_documento_ajuste_view, name='generar_ajuste_factura'),

    #path('detalle/<int:factura_id>/', views.detalle_factura_view, name='detalle_factura'),
    path('listar_facturas/', views.factura_list, name='listar_facturas'),

    path('facturas_mes/', views.select_tipo_facturas_mes_home, name='select_tipo_facturas_mes_home'),
    path('documentos_pendientes/', views.listar_documentos_pendientes, name='listar_documentos_pendientes'),
    path('almacenar_documentos_pendientes/', views.listar_documentos_pendientes, name='almacenar_documentos_pendientes'),


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
    path("fe/factura/<int:factura_id>/termica/", factura_termica, name="factura_termica"),

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
    path("configuracion/empresa/", views.configurar_empresa_view, name="configurar_empresa"),
    
    #LISTADO DE PRODUCTOS
    path('obtener-listado-productos/', views.obtener_listado_productos_view, name='obtener_listado_productos_view'),

    #URLS DE EXPORTACION
    path('exportacion/excel/', views_ventas.exportar_facturas_excel, name='exportar_facturas_excel'),
    path('exportacion/pdf/', views_ventas.exportar_facturas_pdf, name='exportar_facturas_pdf'),
    
    #Contingencia
    path('listar_contingencias/', views.contingencia_list, name='listar_contingencias'),
    path('contingencia-dte/', views.contingencia_dte_unificado_view, name='contingencia_dte_unificado'),
    path('enviar-contingencias-dte/', views.contingencias_dte_view, name='contingencias_dte'),
    path('finalizar-contingencias/', views.finalizar_contigencia_view, name='finalizar_contigencia'),
    #path('procesar-reintento-envio-dte/', views.procesar_respuesta_view, name='procesar_respuesta'),
    
    #Lotes
    path('lote-contingencia-dte/<int:contingencia_id>/', views.lote_contingencia_dte_view, name='lote_contingencia_dte'),
    path('enviar-lote-unificado/', views.envio_dte_unificado_view, name='envio_dte_unificado'),
    path('enviar-lotes/', views.lotes_dte_view, name='lotes_dte'),
    path('enviar-motivo-evento/', views.motivo_contingencia_view, name='enviar_motivo'),
    
    #ENVIO DE CORREO(DOCUMENTOS ELECTRONICOS)
    path('enviar-correo/<int:factura_id>/', views.enviar_correo_individual_view, name='enviar_correo_indiv'),

]

urlpatterns += [
    # Home de Ventas
    path('ventas/', views_ventas.ventas_home, name='ventas_home'),

    path('api/productos/', views_ventas.api_productos, name='api_productos'),

    # Clientes
    path('ventas/clientes/', views_ventas.clientes_list, name='clientes_list'),
    path('ventas/clientes/nuevo/', views_ventas.clientes_crear, name='clientes_crear'),
    path('ventas/clientes/<int:pk>/editar/', views_ventas.clientes_editar, name='clientes_editar'),
    path('ventas/clientes/<int:pk>/eliminar/', views_ventas.clientes_eliminar, name='clientes_eliminar'),

    # Catálogo de productos (de INVENTARIO.Producto)
    path('ventas/catalogo/', views_ventas.catalogo_productos, name='catalogo_productos'),

    # Carrito por cliente (session-based)
    path('ventas/carrito/<int:receptor_id>/cotizacion/', views_ventas.carrito_cotizacion, name='carrito_cotizacion'),
    path('carrito/', views_ventas.carrito_ver, name='carrito_ver'),
    path('carrito/agregar/', views_ventas.carrito_agregar, name='carrito_agregar'),
    path('carrito/actualizar/', views_ventas.carrito_actualizar, name='carrito_actualizar'),
    path('carrito/quitar/', views_ventas.carrito_quitar, name='carrito_quitar'),
    path('carrito/vaciar/', views_ventas.carrito_vaciar, name='carrito_vaciar'),
    path('carrito/facturar/', views_ventas.carrito_facturar, name='carrito_facturar'),
    # opcional: atajo para “agregar y abrir carrito”
    path('carrito/add-go/', views_ventas.carrito_add_go, name='carrito_add_go'),

    # Ventas (usa tus modelos FacturaElectronica / FacturaSujetoExcluidoElectronica)
    path('ventas/lista/', views_ventas.ventas_list, name='ventas_list'),
    path('ventas/<int:factura_id>/', views_ventas.venta_detalle, name='venta_detalle'),  # redirige al detalle que ya tienes

    # Devoluciones de ventas
    path('ventas/<int:factura_id>/devolucion/', views_ventas.devolucion_crear, name='devolucion_crear'),
    path('ventas/devoluciones/', views_ventas.devoluciones_list, name='devoluciones_list'),

    # Reportes de ventas
    path("reporte/contabilidad/", views_ventas.reporte_contabilidad_view, name="reporte_contabilidad"),
    path("reporte/facturacion/", views_ventas.reporte_facturacion_view, name="reporte_facturacion"),


]