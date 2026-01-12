from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

from AUTENTICACION import views_setup

urlpatterns = [

    path('', views.dashboard, name='index'),  # URL raíz que carga la vista index
    path('setup/', views_setup.setup_wizard, name='setup_wizard'),  # 👈 agrega la ruta de setup

    path('', views.dashboard, name='index'),  # URL raíz que carga la vista index
    path('admin/', admin.site.urls),
    path('rrhh/', include('RRHH.urls')),
    path('fe/', include('FE.urls')),
    path('contabilidad/', include('CONTABILIDAD.urls')),
    path('informatica/', include('INFORMATICA.urls')),
    path('inventario/', include('INVENTARIO.urls')),
    path('restaurante/', include('RESTAURANTE.urls')),
    
    #path('dte/', include('FE.dte.urls')),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("autentications/", include("AUTENTICACION.urls")),
    path('select2/', include('django_select2.urls')),

    # Incluir las rutas de la API (asegúrate de ajustar 'fe.urls' al nombre correcto de tu app)
    # path('api/', include('FE.urls_api')),
    # path('api/autenticacion/', include('AUTENTICACION.urls_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)