from django.urls import path

from RESTAURANTE.views import views_caja_y_cajeros, views_cocineros, views_comandas, views_config_restaurante, views_mesas, views_meseros, views_pedidos, views_cuentas

urlpatterns = [
    # categorias para el menu
    path('categorias', views_config_restaurante.listar_categorias, name='categorias-menu'),
    path('categoria/nueva', views_config_restaurante.crear_categoria, name='crear-categoria'),
    path('categoria/<int:pk>/editar/', views_config_restaurante.editar_categoria, name='editar-categoria'),
    path('categoria/<int:pk>/eliminar/', views_config_restaurante.eliminar_categoria, name='eliminar-categoria'), 
    
    # Menu/Platillod
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
 
    # Areas restaurante
    path('areas', views_config_restaurante.listar_areas, name='areas'),
    path('area/nuevo', views_config_restaurante.crear_area, name='crear-area'),
    path('area/<int:pk>/eliminar/', views_config_restaurante.eliminar_area, name='eliminar-area'),
    path('area/<int:pk>/editar/', views_config_restaurante.editar_area, name='editar-area'),
    
    # Areas cocina
    path('areas-cocina', views_config_restaurante.listar_areas_cocina, name='areas-cocina'),
    path('area-cocina/nuevo', views_config_restaurante.crear_area_cocina, name='crear-area-cocina'),
    path('area-cocina/<int:pk>/eliminar/', views_config_restaurante.eliminar_area_cocina, name='eliminar-area-cocina'),
    path('area-cocina/<int:pk>/editar/', views_config_restaurante.editar_area_cocina, name='editar-area-cocina'),
    
    # Mesas
    path('mesas', views_mesas.listar_mesas, name='mesas-lista'),  
     path('mesas/cambiar_estado_mesa/<int:pk>/<str:estado>/', views_mesas.cambiar_estado_mesa, name='cambiar_estado_mesa'),
    path('mesa/crear', views_mesas.crear_mesa, name='crear-mesa'),    
    path('mesa/<int:pk>/editar', views_mesas.editar_mesa, name='editar-mesa'),    
    path('mesa/<int:pk>/eliminar', views_mesas.eliminar_mesa, name='eliminar-mesa'),    
    
    #Asignacion mesas
    path('asignaciones', views_mesas.listar_asignaciones, name='asignaciones-lista'),    
    path('mesa/mesero/asignar', views_mesas.asignar_mesa_a_mesero, name='asignar-mesa-a-mesero'),    
    path('asignacion/<int:pk>/editar', views_mesas.editar_asignacion_mesa_a_mesero, name='editar-asignacion-mesa-a-mesero'),   
    path('asignacion/<int:pk>/eliminar', views_mesas.eliminar_asignacion_mesa_a_mesero, name='eliminar-asignacion-mesa-a-mesero'),     
    
    #Pedidos
    path("pedido/<int:mesa_id>/tomar/", views_pedidos.tomar_pedido, name="tomar_pedido"),
    path("pedidos/crear-desde-mesa/", views_pedidos.pedido_crear_desde_mesa, name="pedido_crear_desde_mesa"),
    path("pedido/<int:pedido_id>/agregar/", views_pedidos.pedido_agregar_item, name="pedido_agregar_item"),
    path("pedido/<int:pedido_id>/quitar/<int:detalle_id>/", views_pedidos.pedido_quitar_item, name="pedido_quitar_item"),
    path("pedidos/pedido/<int:pk>/", views_pedidos.ver_pedido_mesa, name="ver_pedido_mesa"),
    path('entregar/<int:mesa_id>/', views_pedidos.entregar_pedido, name='entregar_pedido'),
    
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

    # Pagos de cuenta
    path('mesa/<int:mesa_id>/solicitar-cuenta/', views_pedidos.solicitar_cuenta, name='solicitar_cuenta'),
    path("mesa/<int:mesa_id>/checkout/", views_pedidos.pedido_checkout, name="pedido-checkout"),
    path("pedido/<int:pedido_id>/split/", views_pedidos.pedido_split, name="pedido-split"),
    path("pedido/<int:pedido_id>/pagar/", views_pedidos.enviar_facturacion, name="enviar-facturacion"),
    path("detalle/mover/", views_pedidos.mover_detalle, name="mover_detalle"), # para cuentas separads
    path('cuenta/<int:cuenta_id>/pagar/', views_pedidos.cuenta_pagar, name='cuenta_pagar'),
    path('cuenta/<int:cuenta_id>/<str:estado>/cambiar-estado/', views_cuentas.cambiar_estado_cuenta, name='cambiar-estado-cuenta'),
    path('pedido/<int:pedido_id>/nueva-cuenta/', views_pedidos.crear_cuenta_extra, name='crear-cuenta-extra'),
    path("pedido/<int:pedido_id>/confirmar-division/", views_pedidos.confirmar_division, name="pedido-confirmar-division"),
    path("cuenta/<int:cuenta_id>/facturar/", views_pedidos.enviar_facturacion_cuenta, name="cuenta-facturar"),
    path("cuenta/<int:cuenta_id>/cambio-nombre/", views_pedidos.cambio_nombre_cuenta, name="cambio_nombre_cuenta"),
    path("cuenta/<int:cuenta_id>/eliminar-cuenta/", views_pedidos.eliminar_cuenta_extra, name="eliminar_cuenta_extra"),
    
    # Caja
    path("caja/", views_caja_y_cajeros.apertura_caja, name="caja"),
    path("caja/dashboard/", views_caja_y_cajeros.caja_dashboard, name="caja-dashboard"),
    path("caja/movimiento/", views_caja_y_cajeros.caja_registrar_movimiento, name="caja-movimiento"),
    path('caja/cierre/', views_caja_y_cajeros.cierre_caja, name='cierre-caja'),

    # Billetes y monedas
    path("billetes-monedas/", views_caja_y_cajeros.billetes_y_monedas_list, name="billetes-y-monedas-list"),
    path("billetes-monedas/crear/", views_caja_y_cajeros.billetes_y_monedas_crear, name="billetes-y-monedas-crear"),
    path("billetes-monedas/<int:pk>/editar/", views_caja_y_cajeros.billetes_y_monedas_editar, name="billetes-y-monedas-editar"),
    path("billetes-monedas/<int:pk>/eliminar/", views_caja_y_cajeros.billetes_y_monedas_eliminar, name="billetes-y-monedas-eliminar"),

    # Cajero
    path("cajeros", views_caja_y_cajeros.listar_cajeros, name="cajero-lista"),
    path("cajero/nuevo", views_caja_y_cajeros.crear_cajero, name="crear-cajero"),
    path("cajero/<int:pk>/eliminar/", views_caja_y_cajeros.eliminar_cajero, name="eliminar-cajero"),
    path("cajero/<int:pk>/editar/", views_caja_y_cajeros.editar_cajero, name="editar-cajero"),
]