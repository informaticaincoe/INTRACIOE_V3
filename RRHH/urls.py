from django.urls import path
from . import views

urlpatterns = [
    
    path('departamentos/', views.departamento_list, name='departamento_list'),
    path('departamentos/crear/', views.departamento_create, name='departamento_create'),
    path('departamentos/editar/<int:pk>/', views.departamento_update, name='departamento_update'),
    path('departamentos/eliminar/<int:pk>/', views.departamento_delete, name='departamento_delete'),

    path('cargos/', views.cargo_list, name='cargo_list'),
    path('cargos/crear/', views.cargo_create, name='cargo_create'),
    path('cargos/editar/<int:pk>/', views.cargo_update, name='cargo_update'),
    path('cargos/eliminar/<int:pk>/', views.cargo_delete, name='cargo_delete'),

    path('empleados/', views.empleado_list, name='empleado_list'),
    path('empleados/crear/', views.empleado_create, name='empleado_create'),
    path('empleados/editar/<int:pk>/', views.empleado_update, name='empleado_update'),
    path('empleados/eliminar/<int:pk>/', views.empleado_delete, name='empleado_delete'),
    path('cargar_empleados/', views.cargar_empleados_desde_xlsx, name='cargar_empleados_desde_xlsx'),

    path('boletas_pago/', views.boleta_pago_list, name='boleta_pago_list'),
    path('boletas_pago/crear/', views.boleta_pago_create, name='boleta_pago_create'),
    path('boletas_pago/editar/<int:pk>/', views.boleta_pago_update, name='boleta_pago_update'),
    path('boletas_pago/eliminar/<int:pk>/', views.boleta_pago_delete, name='boleta_pago_delete'),

    path('cargar_boletas/', views.cargar_boletas, name='cargar_boletas'),
    path('enviar_boletas_masivo/', views.enviar_boletas_masivo, name='enviar_boletas_masivo'),
    path('enviar_boleta/<int:empleado_id>/', views.enviar_boleta_individual, name='enviar_boleta_individual'),

    path('acciones_boletas_pago/', views.acciones_boleta_pago_list, name='acciones_boleta_pago_list'),
    path('acciones_enviar_boletas_masivo/', views.acciones_enviar_boletas_masivo, name='acciones_enviar_boletas_masivo'),
]