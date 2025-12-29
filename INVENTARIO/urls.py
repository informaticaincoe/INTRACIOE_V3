from django.urls import path

from .api_views import (
        # PRODUCTOS Y SERVICIOS
    AlmacenesDetailAPIView,
    DetallesPorCompraView,
    ProductoListAPIView,
    ProductoDetailAPIView,
    ProductoCreateAPIView,
    ProductoProveedorCreateAPIView,
    ProductoProveedorDestroyAPIView,
    ProductoProveedorRetrieveAPIView,
    ProductoProveedorUpdateAPIView,
    ProductoUpdateAPIView,
    ProductoDestroyAPIView,
    ProductosPorIdProveedorListAPIView,
    ProductosProveedorListAPIView,

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
    
    ############# PRODUCTOS Y SERVICIOS PARA SUJETO EXCLUIDO #############
    path('api/productos-proveedor/', ProductosProveedorListAPIView.as_view(), name='producto-proveedor-list'),
    path('api/proveedor/<int:proveedor_id>/productos/', ProductosPorIdProveedorListAPIView.as_view(), name='productos-por-proveedor-list'),
    path('api/productos-proveedor/crear/', ProductoProveedorCreateAPIView.as_view(), name='producto-proveedor-create'),
    path('api/productos-proveedor/<int:pk>/', ProductoProveedorRetrieveAPIView.as_view(), name='producto-proveedor-detail'),
    path('api/productos-proveedor/<int:pk>/editar/', ProductoProveedorUpdateAPIView.as_view(), name='producto-proveedor-update'),
    path('api/productos-proveedor/<int:pk>/eliminar/', ProductoProveedorDestroyAPIView.as_view(), name='producto-proveedor-destroy'),

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
    path('api/almacenes/<int:pk>/', AlmacenesDetailAPIView.as_view(), name='almacene-detail'),
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
    path('api/compras/<int:compra_id>/detalles/', DetallesPorCompraView.as_view(), name='compra-detalles'),
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

    path('', views.inv_home, name='inv-home'),

    # Compras
    path('compras/', views.listar_compras, name='compras-lista'),
    path('compras/nueva/', views.crear_compra, name='compras-crear'),
    path('compras/<int:pk>/', views.detalle_compra, name='compras-detalle'),
    path('compras/<int:pk>/editar/', views.editar_compra, name='compras-editar'),
    path('compras/<int:pk>/eliminar/', views.eliminar_compra, name='compras-eliminar'),
    path('compras/<int:pk>/marcar-pagado/', views.marcar_compra_pagado, name='compras-marcar-pagado'),
    path('compras/<int:pk>/marcar-devuelto/', views.marcar_compra_devuelto, name='compras-marcar-devuelto'),

    # Devoluciones de compra
    path('compras/<int:compra_id>/devoluciones/nueva/', views.crear_devolucion_compra, name='dev-compra-crear'),
    path('devoluciones-compra/', views.listar_devoluciones_compra, name='dev-compra-lista'),

    # Proveedores
    path('proveedores/', views.listar_proveedores, name='proveedores-lista'),
    path('proveedores/nuevo/', views.crear_proveedor, name='proveedores-crear'),
    path('proveedores/<int:pk>/', views.detalle_proveedor, name='proveedores-detalle'),
    path('proveedores/<int:pk>/editar/', views.editar_proveedor, name='proveedores-editar'),
    path('proveedores/<int:pk>/eliminar/', views.eliminar_proveedor, name='proveedores-eliminar'),

    # Productos de un proveedor
    path('proveedores/<int:proveedor_id>/productos/nuevo/', views.crear_producto_proveedor, name='prov-prod-crear'),
    path('proveedores/<int:proveedor_id>/productos/<int:pk>/editar/', views.editar_producto_proveedor, name='prov-prod-editar'),
    path('proveedores/<int:proveedor_id>/productos/<int:pk>/eliminar/', views.eliminar_producto_proveedor, name='prov-prod-eliminar'),

    # Endpoint AJAX para Municipios por Departamento
    path('ajax/municipios/', views.municipios_por_departamento, name='ajax-municipios'),

    # Productos
    path('productos/', views.productos_lista, name='inv-productos-lista'),
    path('productos/nuevo/', views.productos_crear, name='inv-productos-crear'),
    path('productos/<int:pk>/editar/', views.productos_editar, name='inv-productos-editar'),
    path('productos/<int:pk>/eliminar/', views.productos_eliminar, name='inv-productos-eliminar'),

    # Movimientos de inventario (Kardex)
    path('movimientos/', views.movimientos_lista, name='inv-movs-lista'),
    path('movimientos/nuevo/', views.movimientos_crear, name='inv-movs-crear'),
    path('movimientos/<int:pk>/editar/', views.movimientos_editar, name='inv-movs-editar'),
    path('movimientos/<int:pk>/eliminar/', views.movimientos_eliminar, name='inv-movs-eliminar'),

    # Categorías
    path('categorias/', views.categorias_lista, name='inv-categorias-lista'),
    path('categorias/nueva/', views.categorias_crear, name='inv-categorias-crear'),
    path('categorias/<int:pk>/editar/', views.categorias_editar, name='inv-categorias-editar'),
    path('categorias/<int:pk>/eliminar/', views.categorias_eliminar, name='inv-categorias-eliminar'),

    # Tipos de unidad de medida (los que usa Producto)
    path('tipos-unidad/', views.tipos_um_lista, name='inv-tiposum-lista'),
    path('tipos-unidad/nuevo/', views.tipos_um_crear, name='inv-tiposum-crear'),
    path('tipos-unidad/<int:pk>/editar/', views.tipos_um_editar, name='inv-tiposum-editar'),
    path('tipos-unidad/<int:pk>/eliminar/', views.tipos_um_eliminar, name='inv-tiposum-eliminar'),

    # URLs Unidades de Medida
    path('unidades/', views.listar_unidades_medida, name='unidades-lista'),
    path('unidades/nuevo/', views.crear_unidad_medida, name='crear-unidad'),
    path('unidades/editar/<int:pk>/', views.editar_unidad_medida, name='editar-unidad'),
    path('unidades/eliminar/<int:pk>/', views.eliminar_unidad_medida, name='eliminar-unidad'),

    # Impuestos
    path('impuestos/', views.impuestos_lista, name='inv-impuestos-lista'),
    path('impuestos/nuevo/', views.impuestos_crear, name='inv-impuestos-crear'),
    path('impuestos/<int:pk>/editar/', views.impuestos_editar, name='inv-impuestos-editar'),
    path('impuestos/<int:pk>/eliminar/', views.impuestos_eliminar, name='inv-impuestos-eliminar'),

    # Almacenes
    path('almacenes/', views.almacenes_lista, name='inv-almacenes-lista'),
    path('almacenes/nuevo/', views.almacenes_crear, name='inv-almacenes-crear'),
    path('almacenes/<int:pk>/editar/', views.almacenes_editar, name='inv-almacenes-editar'),
    path('almacenes/<int:pk>/eliminar/', views.almacenes_eliminar, name='inv-almacenes-eliminar'),

]