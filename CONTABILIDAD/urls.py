# urls.py
from django.urls import path
from .api_views import AnexoConsumidorFinalAPIView
from . import views

urlpatterns = [
    path('quedans/', views.listar_quedans, name='listar_quedans'),
    path('quedans/pdf/<int:mqdn_id>/', views.generar_pdf_quedan, name='generar_pdf_quedan'),
    path('quedans/envio/<int:mqdn_id>/', views.enviar_quedan, name='enviar_quedan'),
    path('quedans/envio_hoy/', views.enviar_quedan_hoy, name='enviar_quedan_hoy'),
    path('reportes/anexo-consumidor-final/', views.AnexoConsumidorFinalCSV.as_view(), name='anexo-consumidor-final'),
    path('reportes/anexo-contribuyentes/',views.AnexoContribuyentesCSV.as_view(),name='anexo-contribuyentes'),
    path('reportes/anexo-compras/',views.AnexoComprasCSV.as_view(),name='anexo-compras'),

    # URLS DE API
    path('api/anexo-consumidor-final/',AnexoConsumidorFinalAPIView.as_view(),name='api-anexo-consumidor-final'),

    # ── Plan de Cuentas ──
    path('cuentas/',                     views.cuentas_lista,    name='cont-cuentas-lista'),
    path('cuentas/nueva/',               views.cuentas_crear,    name='cont-cuentas-crear'),
    path('cuentas/<int:pk>/editar/',     views.cuentas_editar,   name='cont-cuentas-editar'),
    path('cuentas/<int:pk>/eliminar/',   views.cuentas_eliminar, name='cont-cuentas-eliminar'),

    # ── Asientos Contables ──
    path('asientos/',                      views.asientos_lista,     name='cont-asientos-lista'),
    path('asientos/nuevo/',                views.asientos_crear,     name='cont-asientos-crear'),
    path('asientos/<int:pk>/',             views.asientos_ver,       name='cont-asientos-ver'),
    path('asientos/<int:pk>/editar/',      views.asientos_editar,    name='cont-asientos-editar'),
    path('asientos/<int:pk>/confirmar/',   views.asientos_confirmar, name='cont-asientos-confirmar'),
    path('asientos/<int:pk>/eliminar/',    views.asientos_eliminar,  name='cont-asientos-eliminar'),

    # ── Cuentas por Cobrar ──
    path('cxc/',                              views.cpc_lista,            name='cont-cpc-lista'),
    path('cxc/nueva/',                        views.cpc_crear,            name='cont-cpc-crear'),
    path('cxc/<int:pk>/',                     views.cpc_detalle,          name='cont-cpc-detalle'),
    path('cxc/<int:pk>/pago/',                views.cpc_registrar_pago,   name='cont-cpc-pago'),
    path('cxc/<int:pk>/anular/',              views.cpc_anular,           name='cont-cpc-anular'),

    # ── Cuentas por Pagar ──
    path('cxp/',                              views.cpp_lista,            name='cont-cpp-lista'),
    path('cxp/nueva/',                        views.cpp_crear,            name='cont-cpp-crear'),
    path('cxp/<int:pk>/',                     views.cpp_detalle,          name='cont-cpp-detalle'),
    path('cxp/<int:pk>/pago/',                views.cpp_registrar_pago,   name='cont-cpp-pago'),
    path('cxp/<int:pk>/anular/',              views.cpp_anular,           name='cont-cpp-anular'),
]
