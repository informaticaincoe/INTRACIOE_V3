from django.urls import path

from RESTAURANTE.views import views_cocineros, views_comandas, views_config_restaurante, views_mesas, views_meseros, views_pedidos
from RESTAURANTE.views.views_cuentas import cambiar_estado_cuenta


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
    path("mesero/login/", views_meseros.login_mesero, name="login_mesero"),
    path('meseros', views_meseros.listar_meseros, name='meseros-lista'),
    path('mesero/nuevo', views_meseros.crear_mesero, name='crear-mesero'),
    path('mesero/<int:pk>/eliminar/', views_meseros.eliminar_mesero, name='eliminar-mesero'),
    path('mesero/<int:pk>/editar/', views_meseros.editar_mesero, name='editar-mesero'),
 
    # Area
    path('areas', views_config_restaurante.listar_areas, name='areas'),
    path('area/nuevo', views_config_restaurante.crear_area, name='crear-area'),
    path('area/<int:pk>/eliminar/', views_config_restaurante.eliminar_area, name='eliminar-area'),
    path('area/<int:pk>/editar/', views_config_restaurante.editar_area, name='editar-area'),
    
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
    path("pedidos/crear-desde-mesa/", views_pedidos.pedido_crear_desde_mesa, name="pedido_crear_desde_mesa"),
    path("pedido/<int:pedido_id>/agregar/", views_pedidos.pedido_agregar_item, name="pedido_agregar_item"),
    path("pedido/<int:pedido_id>/quitar/<int:detalle_id>/", views_pedidos.pedido_quitar_item, name="pedido_quitar_item"),
    path("pedido/<int:pedido_id>/cerrar/", views_pedidos.pedido_cerrar, name="pedido_cerrar"),
    #Pagos
    # path("pedido/<int:pedido_id>/cerrar/", views_pedidos.pedido_cerrar, name="pedido_cerrar"),
    
    path("pedidos/pedido/<int:pk>/", views_pedidos.ver_pedido_mesa, name="ver_pedido_mesa"),
    
    # Cocineros
    path("cocinero/login/", views_cocineros.login_cocinero, name="login_cocinero"),
    path("cocineros", views_cocineros.listar_cocineros, name="cocineros-lista"),
    path("cocinero/nuevo", views_cocineros.crear_cocinero, name="crear-cocinero"),
    path("cocinero/<int:pk>/eliminar/", views_cocineros.eliminar_cocinero, name="eliminar-cocinero"),
    path("cocinero/<int:pk>/editar/", views_cocineros.editar_cocinero, name="editar-cocinero"),

    # Comandas
    path("cocina/comanda/", views_comandas.comanda_cocina, name="comanda-cocina"),
    path("cocina/comanda/<int:id>/preparacion/", views_comandas.comanda_en_preparacion, name="comanda-item-preparacion"),
    path("cocina/comanda/<int:id>/listo/", views_comandas.comanda_listo, name="comanda-item-listo"),

    path('mesa/<int:mesa_id>/solicitar-cuenta/', views_pedidos.solicitar_cuenta, name='solicitar_cuenta'),
    path("mesa/<int:mesa_id>/checkout/", views_pedidos.pedido_checkout, name="pedido-checkout"),
    path("pedido/<int:pedido_id>/split/", views_pedidos.pedido_split, name="pedido-split"),
    path("pedido/<int:pedido_id>/pagar/", views_pedidos.enviar_facturacion, name="enviar-facturacion"),
    
    path('entregar/<int:mesa_id>/', views_pedidos.entregar_pedido, name='entregar_pedido'),

    path("detalle/mover/", views_pedidos.detalle_mover_a_cuenta, name="detalle-mover-a-cuenta"),

    path('cuenta/<int:cuenta_id>/pagar/', views_pedidos.cuenta_pagar, name='cuenta_pagar'),
    path('pedido/<int:pedido_id>/nueva-cuenta/', views_pedidos.crear_cuenta_extra, name='crear-cuenta-extra'),
    
    path("pedido/<int:pedido_id>/confirmar-division/", views_pedidos.confirmar_division, name="pedido-confirmar-division"),
    path("cuenta/<int:cuenta_id>/facturar/", views_pedidos.enviar_facturacion_cuenta, name="cuenta-facturar"),

    # Agregamos el parámetro <str:estado> al final
    path("cuenta/<int:cuenta_id>/cambiar-estado/<str:estado>/", cambiar_estado_cuenta, name="cambiar-estado-cuenta")

]