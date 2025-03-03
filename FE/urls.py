from django.urls import path
from . import views

#renombrar el archivo
urlpatterns = [
    path("autenticacion/", views.autenticacion, name="autenticacion"),
    path('autenticacion_api/', views.AutenticacionAPIView.as_view(), name='autenticacion-api'),
    

]
