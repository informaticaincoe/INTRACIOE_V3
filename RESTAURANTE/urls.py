from django.urls import path

from RESTAURANTE.views import views_config_restaurante, views_mesas, views_meseros, views_pedidos


urlpatterns = [
    # categorias para el menu
    path('categorias', views_config_restaurante.listar_categorias, name='categorias-menu'),
    path('categoria/nueva', views_config_restaurante.crear_categoria, name='crear-categoria'),
    path('categoria/<int:pk>/editar/', views_config_restaurante.editar_categoria, name='editar-categoria'),
    path('categoria/<int:pk>/eliminar/', views_config_restaurante.eliminar_categoria, name='eliminar-categoria'), 
    
    # Menu
    path('menu', views_config_restaurante.listar_menu, name='menu'),
    path('menu/nueva', views_config_restaurante.crear_menu, name='crear-menu'),
    path('menu/<int:pk>/editar/', views_config_restaurante.editar_menu, name='editar-menu'),
    path('menu/<int:pk>/eliminar/', views_config_restaurante.eliminar_menu, name='eliminar-menu'), 
    
    # Meseros
    path('meseros', views_meseros.listar_meseros, name='meseros-lista'),
    path('mesero/nuevo', views_meseros.crear_mesero, name='crear-mesero'),
    path('mesero/<int:pk>/eliminar/', views_meseros.eliminar_mesero, name='eliminar-mesero'),
    path('mesero/<int:pk>/editar/', views_meseros.editar_mesero, name='editar-mesero'),
 
    # Area
    path('areas', views_config_restaurante.listar_areas, name='areas'),
    path('area/nuevo', views_config_restaurante.crear_area, name='crear-area'),
    path('area/<int:pk>/eliminar/', views_config_restaurante.eliminar_area, name='eliminar-area'),
    path('area/<int:pk>/editar/', views_config_restaurante.editar_area, name='editar-area'),
    path("mesero/login/", views_meseros.login_mesero, name="login_mesero"),
    
    # Mesas
    path('mesas', views_mesas.listar_mesas, name='mesas-lista'),  
    path('mesa/crear', views_mesas.crear_mesa, name='crear-mesa'),    
    path('mesa/<int:pk>/editar', views_mesas.editar_mesa, name='editar-mesa'),    
    path('mesa/<int:pk>/eliminar', views_mesas.eliminar_mesa, name='eliminar-mesa'),    
    
    #Asignacion mesas
    path('mesa/mesero/asignar', views_mesas.asignar_mesa_a_mesero, name='asignar-mesa-a-mesero'),    
    path('asignacion/<int:pk>/editar', views_mesas.editar_asignacion_mesa_a_mesero, name='editar-asignacion-mesa-a-mesero'),   
    path('asignacion/<int:pk>/eliminar', views_mesas.eliminar_asignacion_mesa_a_mesero, name='eliminar-asignacion-mesa-a-mesero'),     
    path('asignaciones', views_mesas.listar_asignaciones, name='asignaciones-lista'),    
    
    #Pedidos
    path('mesas/cambiar_estado_mesa/<int:pk>/<str:estado>/', views_mesas.cambiar_estado_mesa, name='cambiar_estado_mesa'),

    path("pedido/<int:mesa_id>/tomar/", views_pedidos.tomar_pedido, name="tomar_pedido"),
    path("pedido/<int:pedido_id>/agregar/", views_pedidos.pedido_agregar_item, name="pedido_agregar_item"),
    path("pedido/<int:pedido_id>/quitar/<int:detalle_id>/", views_pedidos.pedido_quitar_item, name="pedido_quitar_item"),
    path("pedido/<int:pedido_id>/cerrar/", views_pedidos.pedido_cerrar, name="pedido_cerrar"),
    path("pedidos/crear-desde-mesa/", views_pedidos.pedido_crear_desde_mesa, name="pedido_crear_desde_mesa"),
]