from django.urls import path

from .api_views import AlmacenesListAPIView, ImpuestosListAPIView, ProductoCreateAPIView, ProductoDestroyAPIView, ProductoDetailAPIView, ProductoListAPIView, ProductoUpdateAPIView, TipoItemListAPIView, TiposTributosListAPIView, TributoByTipoListAPIView, TributoDetailsAPIView, TributosListAPIView, UnidadMedidaListAPIView
from . import views

urlpatterns = [


    # -------------------------------
    # Endpoints API REST
    # -------------------------------


    #---------- URLS TRIBUTOS ----------#
    path('api/tipo-tributos/', TiposTributosListAPIView.as_view(), name='tipo_tributos_api'),
    path('api/tributos/tipo/<int:tipo_valor>/', TributoByTipoListAPIView.as_view(), name='tributos_api'),
    path('api/tributo/<int:pk>/', TributoDetailsAPIView.as_view(), name='tributo_api'), 
    path('api/tributos/', TributosListAPIView.as_view(), name='tributo_api'), 


    #----------- PRODUCTOS -----------#
    #URL PRODUCTOS
    
    path('api/productos/', ProductoListAPIView.as_view(), name='api_productos_list'),
    path('api/producto/<int:pk>/', ProductoDetailAPIView.as_view(), name='api_productos_list'),
    path('api/productos/crear/', ProductoCreateAPIView.as_view(), name='api_productos_create'),
    path('api/productos/<int:pk>/editar/', ProductoUpdateAPIView.as_view(), name='api_productos_update'),
    path('api/productos/<int:pk>/eliminar/', ProductoDestroyAPIView.as_view(), name='api_productos_destroy'), 
    path('api/unidad-medida/', UnidadMedidaListAPIView.as_view(), name='unidad_medida_api'), 
    path('api/tipo-item/', TipoItemListAPIView.as_view(), name='tipo_item_api'),
    path('api/almacenes/', AlmacenesListAPIView.as_view(), name='almacenes_api'), 


    #----------- INPUESTOS -----------#
    path('api/impuestos/', ImpuestosListAPIView.as_view(), name='impuestos_api'), 

    # Endpoints API REST
    # -------------------------------

    # Productos
    path('productos/', views.listar_productos, name='productos-lista'),
    path('productos/crear/', views.crear_producto, name='crear-producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar-producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar-producto'),

    # Movimientos de Inventario
    path('inventario/', views.listar_movimientos, name='movimientos-lista'),
    path('inventario/crear/', views.crear_movimiento, name='crear-movimiento'),

    # URLs Categorías
    path('categorias/', views.listar_categorias, name='categorias-lista'),
    path('categorias/nuevo/', views.crear_categoria, name='crear-categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar-categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar-categoria'),

    # URLs Unidades de Medida
    path('unidades/', views.listar_unidades_medida, name='unidades-lista'),
    path('unidades/nuevo/', views.crear_unidad_medida, name='crear-unidad'),
    path('unidades/editar/<int:pk>/', views.editar_unidad_medida, name='editar-unidad'),
    path('unidades/eliminar/<int:pk>/', views.eliminar_unidad_medida, name='eliminar-unidad'),

    # URLs Impuestos
    path('impuestos/', views.listar_impuestos, name='impuestos-lista'),
    path('impuestos/nuevo/', views.crear_impuesto, name='crear-impuesto'),
    path('impuestos/editar/<int:pk>/', views.editar_impuesto, name='editar-impuesto'),
    path('impuestos/eliminar/<int:pk>/', views.eliminar_impuesto, name='eliminar-impuesto'),

    # URLs Almacenes
    path('almacenes/', views.listar_almacenes, name='almacenes-lista'),
    path('almacenes/nuevo/', views.crear_almacen, name='crear-almacen'),
    path('almacenes/editar/<int:pk>/', views.editar_almacen, name='editar-almacen'),
    path('almacenes/eliminar/<int:pk>/', views.eliminar_almacen, name='eliminar-almacen'),
]
