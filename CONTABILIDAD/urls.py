# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('quedans/', views.listar_quedans, name='listar_quedans'),
    path('quedans/pdf/<int:mqdn_id>/', views.generar_pdf_quedan, name='generar_pdf_quedan'),
    path('quedans/envio/<int:mqdn_id>/', views.enviar_quedan, name='enviar_quedan'),
    path('quedans/envio_hoy/', views.enviar_quedan_hoy, name='enviar_quedan_hoy'),
]
