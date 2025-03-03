# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('listar-bases-datos/', views.listar_bases_datos, name='listar_bases_datos'),
    path('estructura/<str:nombre_db>/', views.ver_estructura_base_datos, name='ver_estructura_base_datos'),
    path('estructura/<str:nombre_db>/<str:nombre_tabla>/', views.ver_contenido_tabla, name='ver_estructura_tabla'),
    path('estructura/<str:nombre_db>/buscar_tablas/', views.buscar_tablas, name='buscar_tablas'),
]
