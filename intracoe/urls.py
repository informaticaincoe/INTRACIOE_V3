from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.index, name='index'),  # URL raíz que carga la vista index
    path('admin/', admin.site.urls),
    path('rrhh/', include('RRHH.urls')),
    path('fe/', include('FE.urls')),
    path('contabilidad/', include('CONTABILIDAD.urls')),
    path('informatica/', include('INFORMATICA.urls')),
    path('inventario/', include('INVENTARIO.urls')),
    #path('dte/', include('FE.dte.urls')),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('select2/', include('django_select2.urls')),

    # Incluir las rutas de la API (asegúrate de ajustar 'fe.urls' al nombre correcto de tu app)
    path('api/', include('FE.urls_api')),
]
