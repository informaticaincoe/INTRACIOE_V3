# AUTENTICACION/urls.py
from django.urls import path

from AUTENTICACION import view_groups_and_permissions, views_users

from . import views_setup
from .views import perfil_usuario_view
from . import views as views_usuarios

urlpatterns = [
    path("cuenta/perfil/", perfil_usuario_view, name="perfil_usuario"),

    # Usuarios
    path('usuarios/', views_usuarios.usuarios_list, name='usuarios_list'),
    path('usuarios/crear/', views_usuarios.usuarios_crear, name='usuarios_crear'),
    path('usuarios/<int:pk>/editar/', views_usuarios.usuarios_editar, name='usuarios_editar'),
    path('usuarios/<int:pk>/eliminar/', views_usuarios.usuarios_eliminar, name='usuarios_eliminar'),

    path("setup/", views_setup.setup_wizard, name="setup_wizard"),

    # path("usuarios/", views_users.usuarios_list, name="usuarios_list"),
    # path("usuarios/crear/", views_users.usuarios_crear, name="usuarios_crear"),
    # path("usuarios/<int:pk>/editar/", views_users.usuarios_editar, name="usuarios_editar"),
    # path("usuarios/<int:pk>/eliminar/", views_users.usuarios_eliminar, name="usuarios_eliminar"),

    # endpoints ajax
    path("crear-ambiente/", views_setup.crear_ambiente, name="crear_ambiente"),
    path("crear-municipio/", views_setup.crear_municipio, name="crear_municipio"),
    path("crear-actividad/", views_setup.crear_actividad, name="crear_actividad"),
    path("crear-tipo-establecimiento/", views_setup.crear_tipo_establecimiento, name="crear_tipo_establecimiento"),
    path("crear-departamento/", views_setup.crear_departamento, name="crear_departamento"),
    path("crear-pais/", views_setup.crear_pais, name="crear_pais"),
    path("crear_tipo_documento/", views_setup.crear_tipo_documento, name="crear_tipo_documento"),

    #Grupos
    path("grupos/", view_groups_and_permissions.groups_list, name="group_list"),
    
    path("permisos/", view_groups_and_permissions.permisos_list, name="permisos_list"),
    path("permisos-by-group/", view_groups_and_permissions.permisos_ny_grupo_list, name="permisos_goup_list"),
    
    path("permisos/<int:grupo_id>/editar/", view_groups_and_permissions.editar_permisos_grupo, name="editar_permisos"),
    
    path("permisos/actualizar/", view_groups_and_permissions.actualizar_permiso_ajax, name="actualizar_permiso_ajax"),
    
]
