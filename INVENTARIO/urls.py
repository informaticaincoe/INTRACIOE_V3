from django.urls import path
from . import views

urlpatterns = [
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
