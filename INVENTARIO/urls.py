from django.urls import path

from .api_views import (
        # PRODUCTOS Y SERVICIOS
    ProductoListAPIView,
    ProductoDetailAPIView,
    ProductoCreateAPIView,
    ProductoUpdateAPIView,
    ProductoDestroyAPIView,

    # TIPO TRIBUTOS
    TiposTributosListAPIView,
    TiposTributosCreateAPIView,
    TiposTributosUpdateAPIView,
    TiposTributosDestroyAPIView,
    TributoByTipoListAPIView,
    
    # TRIBUTOS
    TributosListAPIView,
    TributoDetailsAPIView,
    TributoCreateAPIView,
    TributoUpdateAPIView,
    TributoDestroyAPIView,
    
    # UNIDAD DE MEDIDA
    UnidadMedidaListAPIView,
    UnidadMedidaCreateAPIView,
    UnidadMedidaUpdateAPIView,
    UnidadMedidaDestroyAPIView,
    
    # TIPO ITEM
    TipoItemListAPIView,
    TipoItemCreateAPIView,
    TipoItemUpdateAPIView,
    TipoItemDestroyAPIView,
    
    # IMPUESTOS
    ImpuestosListAPIView,
    ImpuestosCreateAPIView,
    ImpuestosUpdateAPIView,
    ImpuestosDestroyAPIView,
    
    # ALMACENES
    AlmacenesListAPIView,
    AlmacenesCreateAPIView,
    AlmacenesUpdateAPIView,
    AlmacenesDestroyAPIView,

    # Proveedores
    ProveedorListAPIView, ProveedorCreateAPIView, ProveedorRetrieveAPIView,
    ProveedorUpdateAPIView, ProveedorDestroyAPIView,
    # Compras
    CompraListAPIView, CompraCreateAPIView, CompraRetrieveAPIView,
    CompraUpdateAPIView, CompraDestroyAPIView,
    # Detalle Compras
    DetalleCompraListAPIView, DetalleCompraCreateAPIView, DetalleCompraRetrieveAPIView,
    DetalleCompraUpdateAPIView, DetalleCompraDestroyAPIView,
    # Movimientos Inventario
    MovimientoInventarioListAPIView, MovimientoInventarioCreateAPIView, MovimientoInventarioRetrieveAPIView,
    MovimientoInventarioUpdateAPIView, MovimientoInventarioDestroyAPIView,
    # Ajustes Inventario
    AjusteInventarioListAPIView, AjusteInventarioCreateAPIView, AjusteInventarioRetrieveAPIView,
    AjusteInventarioUpdateAPIView, AjusteInventarioDestroyAPIView,
    # Devoluciones Venta
    DevolucionVentaListAPIView, DevolucionVentaCreateAPIView, DevolucionVentaRetrieveAPIView,
    DevolucionVentaUpdateAPIView, DevolucionVentaDestroyAPIView,
    # Detalle Devolucion Venta
    DetalleDevolucionVentaListAPIView, DetalleDevolucionVentaCreateAPIView, DetalleDevolucionVentaRetrieveAPIView,
    DetalleDevolucionVentaUpdateAPIView, DetalleDevolucionVentaDestroyAPIView,
    # Devoluciones Compra
    DevolucionCompraListAPIView, DevolucionCompraCreateAPIView, DevolucionCompraRetrieveAPIView,
    DevolucionCompraUpdateAPIView, DevolucionCompraDestroyAPIView,
    # Detalle Devolucion Compra
    DetalleDevolucionCompraListAPIView, DetalleDevolucionCompraCreateAPIView, DetalleDevolucionCompraRetrieveAPIView,
    DetalleDevolucionCompraUpdateAPIView, DetalleDevolucionCompraDestroyAPIView
    )
from . import views

urlpatterns = [
    # -------------------------------
    # Endpoints API REST
    # -------------------------------

    ############# PRODUCTOS Y SERVICIOS #############
    path('api/productos/', ProductoListAPIView.as_view(), name='producto-list'),
    path('api/productos/crear/', ProductoCreateAPIView.as_view(), name='producto-create'),
    path('api/productos/<int:pk>/', ProductoDetailAPIView.as_view(), name='producto-detail'),
    path('api/productos/<int:pk>/editar/', ProductoUpdateAPIView.as_view(), name='producto-update'),
    path('api/productos/<int:pk>/eliminar/', ProductoDestroyAPIView.as_view(), name='producto-destroy'),

    ############# TIPO TRIBUTOS #############
    path('api/tipo-tributos/', TiposTributosListAPIView.as_view(), name='tipos-tributos-list'),
    path('api/tipo-tributos/crear/', TiposTributosCreateAPIView.as_view(), name='tipos-tributos-create'),
    path('api/tipo-tributos/<int:pk>/editar/', TiposTributosUpdateAPIView.as_view(), name='tipos-tributos-update'),
    path('api/tipo-tributos/<int:pk>/eliminar/', TiposTributosDestroyAPIView.as_view(), name='tipos-tributos-destroy'),
    # Lista tributos filtrados por el tipo (parámetro en la URL)
    path('api/tipo-tributos/<int:tipo_valor>/tributos/', TributoByTipoListAPIView.as_view(), name='tributos-by-tipo'),

    ############# TRIBUTOS #############
    path('api/tributo/', TributosListAPIView.as_view(), name='tributos-list'),
    path('api/tributo/crear/', TributoCreateAPIView.as_view(), name='tributo-create'),
    path('api/tributo/<int:pk>/', TributoDetailsAPIView.as_view(), name='tributo-detail'),
    path('api/tributo/<int:pk>/editar/', TributoUpdateAPIView.as_view(), name='tributo-update'),
    path('api/tributo/<int:pk>/eliminar/', TributoDestroyAPIView.as_view(), name='tributo-destroy'),

    ############# UNIDAD DE MEDIDA #############
    path('api/unidades-medida/', UnidadMedidaListAPIView.as_view(), name='unidad-medida-list'),
    path('api/unidades-medida/crear/', UnidadMedidaCreateAPIView.as_view(), name='unidad-medida-create'),
    path('api/unidades-medida/<int:pk>/editar/', UnidadMedidaUpdateAPIView.as_view(), name='unidad-medida-update'),
    path('api/unidades-medida/<int:pk>/eliminar/', UnidadMedidaDestroyAPIView.as_view(), name='unidad-medida-destroy'),

    ############# TIPO ITEM #############
    path('api/tipo-item/', TipoItemListAPIView.as_view(), name='tipo-item-list'),
    path('api/tipo-item/crear/', TipoItemCreateAPIView.as_view(), name='tipo-item-create'),
    path('api/tipo-item/<int:pk>/editar/', TipoItemUpdateAPIView.as_view(), name='tipo-item-update'),
    path('api/tipo-item/<int:pk>/eliminar/', TipoItemDestroyAPIView.as_view(), name='tipo-item-destroy'),

    ############# IMPUESTOS #############
    path('api/impuestos/', ImpuestosListAPIView.as_view(), name='impuestos-list'),
    path('api/impuestos/crear/', ImpuestosCreateAPIView.as_view(), name='impuestos-create'),
    path('api/impuestos/<int:pk>/editar/', ImpuestosUpdateAPIView.as_view(), name='impuestos-update'),
    path('api/impuestos/<int:pk>/eliminar/', ImpuestosDestroyAPIView.as_view(), name='impuestos-destroy'),

    ############# ALMACENES #############
    path('api/almacenes/', AlmacenesListAPIView.as_view(), name='almacenes-list'),
    path('api/almacenes/crear/', AlmacenesCreateAPIView.as_view(), name='almacenes-create'),
    path('api/almacenes/<int:pk>/editar/', AlmacenesUpdateAPIView.as_view(), name='almacenes-update'),
    path('api/almacenes/<int:pk>/eliminar/', AlmacenesDestroyAPIView.as_view(), name='almacenes-destroy'),

    ##############################
    # PROVEEDORES
    ##############################
    path('api/proveedores/', ProveedorListAPIView.as_view(), name='proveedor-list'),
    path('api/proveedores/crear/', ProveedorCreateAPIView.as_view(), name='proveedor-create'),
    path('api/proveedores/<int:pk>/', ProveedorRetrieveAPIView.as_view(), name='proveedor-detail'),
    path('api/proveedores/<int:pk>/editar/', ProveedorUpdateAPIView.as_view(), name='proveedor-update'),
    path('api/proveedores/<int:pk>/eliminar/', ProveedorDestroyAPIView.as_view(), name='proveedor-destroy'),
    
    ##############################
    # COMPRAS
    ##############################
    path('api/compras/', CompraListAPIView.as_view(), name='compra-list'),
    path('api/compras/crear/', CompraCreateAPIView.as_view(), name='compra-create'),
    path('api/compras/<int:pk>/', CompraRetrieveAPIView.as_view(), name='compra-detail'),
    path('api/compras/<int:pk>/editar/', CompraUpdateAPIView.as_view(), name='compra-update'),
    path('api/compras/<int:pk>/eliminar/', CompraDestroyAPIView.as_view(), name='compra-destroy'),

    ##############################
    # DETALLE DE COMPRAS
    ##############################
    path('api/detalle-compra/', DetalleCompraListAPIView.as_view(), name='detalle-compra-list'),
    path('api/detalle-compra/crear/', DetalleCompraCreateAPIView.as_view(), name='detalle-compra-create'),
    path('api/detalle-compra/<int:pk>/', DetalleCompraRetrieveAPIView.as_view(), name='detalle-compra-detail'),
    path('api/detalle-compra/<int:pk>/editar/', DetalleCompraUpdateAPIView.as_view(), name='detalle-compra-update'),
    path('api/detalle-compra/<int:pk>/eliminar/', DetalleCompraDestroyAPIView.as_view(), name='detalle-compra-destroy'),

    ##############################
    # MOVIMIENTOS DE INVENTARIO
    ##############################
    path('api/movimientos-inventario/', MovimientoInventarioListAPIView.as_view(), name='movimiento-inventario-list'),
    path('api/movimientos-inventario/crear/', MovimientoInventarioCreateAPIView.as_view(), name='movimiento-inventario-create'),
    path('api/movimientos-inventario/<int:pk>/', MovimientoInventarioRetrieveAPIView.as_view(), name='movimiento-inventario-detail'),
    path('api/movimientos-inventario/<int:pk>/editar/', MovimientoInventarioUpdateAPIView.as_view(), name='movimiento-inventario-update'),
    path('api/movimientos-inventario/<int:pk>/eliminar/', MovimientoInventarioDestroyAPIView.as_view(), name='movimiento-inventario-destroy'),

    ##############################
    # AJUSTES DE INVENTARIO
    ##############################
    path('api/ajustes-inventario/', AjusteInventarioListAPIView.as_view(), name='ajuste-inventario-list'),
    path('api/ajustes-inventario/crear/', AjusteInventarioCreateAPIView.as_view(), name='ajuste-inventario-create'),
    path('api/ajustes-inventario/<int:pk>/', AjusteInventarioRetrieveAPIView.as_view(), name='ajuste-inventario-detail'),
    path('api/ajustes-inventario/<int:pk>/editar/', AjusteInventarioUpdateAPIView.as_view(), name='ajuste-inventario-update'),
    path('api/ajustes-inventario/<int:pk>/eliminar/', AjusteInventarioDestroyAPIView.as_view(), name='ajuste-inventario-destroy'),

    ##############################
    # DEVOLUCIONES DE VENTA
    ##############################
    path('api/devoluciones-venta/', DevolucionVentaListAPIView.as_view(), name='devolucion-venta-list'),
    path('api/devoluciones-venta/crear/', DevolucionVentaCreateAPIView.as_view(), name='devolucion-venta-create'),
    path('api/devoluciones-venta/<int:pk>/', DevolucionVentaRetrieveAPIView.as_view(), name='devolucion-venta-detail'),
    path('api/devoluciones-venta/<int:pk>/editar/', DevolucionVentaUpdateAPIView.as_view(), name='devolucion-venta-update'),
    path('api/devoluciones-venta/<int:pk>/eliminar/', DevolucionVentaDestroyAPIView.as_view(), name='devolucion-venta-destroy'),

    ##############################
    # DETALLE DE DEVOLUCIONES DE VENTA
    ##############################
    path('api/detalle-devolucion-venta/', DetalleDevolucionVentaListAPIView.as_view(), name='detalle-devolucion-venta-list'),
    path('api/detalle-devolucion-venta/crear/', DetalleDevolucionVentaCreateAPIView.as_view(), name='detalle-devolucion-venta-create'),
    path('api/detalle-devolucion-venta/<int:pk>/', DetalleDevolucionVentaRetrieveAPIView.as_view(), name='detalle-devolucion-venta-detail'),
    path('api/detalle-devolucion-venta/<int:pk>/editar/', DetalleDevolucionVentaUpdateAPIView.as_view(), name='detalle-devolucion-venta-update'),
    path('api/detalle-devolucion-venta/<int:pk>/eliminar/', DetalleDevolucionVentaDestroyAPIView.as_view(), name='detalle-devolucion-venta-destroy'),

    ##############################
    # DEVOLUCIONES DE COMPRA
    ##############################
    path('api/devoluciones-compra/', DevolucionCompraListAPIView.as_view(), name='devolucion-compra-list'),
    path('api/devoluciones-compra/crear/', DevolucionCompraCreateAPIView.as_view(), name='devolucion-compra-create'),
    path('api/devoluciones-compra/<int:pk>/', DevolucionCompraRetrieveAPIView.as_view(), name='devolucion-compra-detail'),
    path('api/devoluciones-compra/<int:pk>/editar/', DevolucionCompraUpdateAPIView.as_view(), name='devolucion-compra-update'),
    path('api/devoluciones-compra/<int:pk>/eliminar/', DevolucionCompraDestroyAPIView.as_view(), name='devolucion-compra-destroy'),

    ##############################
    # DETALLE DE DEVOLUCIONES DE COMPRA
    ##############################
    path('api/detalle-devolucion-compra/', DetalleDevolucionCompraListAPIView.as_view(), name='detalle-devolucion-compra-list'),
    path('api/detalle-devolucion-compra/crear/', DetalleDevolucionCompraCreateAPIView.as_view(), name='detalle-devolucion-compra-create'),
    path('api/detalle-devolucion-compra/<int:pk>/', DetalleDevolucionCompraRetrieveAPIView.as_view(), name='detalle-devolucion-compra-detail'),
    path('api/detalle-devolucion-compra/<int:pk>/editar/', DetalleDevolucionCompraUpdateAPIView.as_view(), name='detalle-devolucion-compra-update'),
    path('api/detalle-devolucion-compra/<int:pk>/eliminar/', DetalleDevolucionCompraDestroyAPIView.as_view(), name='detalle-devolucion-compra-destroy'),


    # Endpoints API REST
    # -------------------------------
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
