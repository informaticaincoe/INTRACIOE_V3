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
]
