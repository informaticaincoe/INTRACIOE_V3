
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminOrSupervisor, IsAuthenticatedReadOrAdminWrite

from .serializers import (
    AlmacenSerializer, DetalleCompraReadSerializer, ImpuestoSerializer, ProductoSerializer, ProductosProveedorSerializer, TipoItemSerializer,
    TipoUnidadMedidaSerializer, TiposTributosSerializer, TributosSerializer, 
    ProveedorSerializer, CompraSerializer, DetalleCompraSerializer,
    MovimientoInventarioSerializer, AjusteInventarioSerializer,
    DevolucionVentaSerializer, DetalleDevolucionVentaSerializer,
    DevolucionCompraSerializer, DetalleDevolucionCompraSerializer
    )
from .models import (
    Almacen, Impuesto, Producto, ProductoProveedor, TipoItem, TipoTributo, TipoUnidadMedida, Tributo,
    Proveedor, Compra, DetalleCompra, MovimientoInventario, AjusteInventario,
    DevolucionVenta, DetalleDevolucionVenta, DevolucionCompra, DetalleDevolucionCompra
    )
from django.db.models import Q

class StandardResultsSetPagination(PageNumberPagination):
    # Número de ítems por página por defecto
    page_size = 10
    # Permitir al cliente cambiar el tamaño de página con ?page_size=
    page_size_query_param = 'page_size'
    # Límite máximo que puede pedir
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'current_page': self.page.number,
            'has_next': self.page.has_next(),
            'has_previous': self.page.has_previous(),
            'results': data
        })
     
######################################################
# PRODUCTOS Y SERVICIOS
######################################################

# Listar productos con filtrado por código o descripción
class ProductoListAPIView(generics.ListAPIView):
    serializer_class = ProductoSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Producto.objects.all()

        # 1) Filtrar por tipo de ítem (por su código)
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            qs = qs.filter(tipo_item__codigo=tipo)
            # si prefieres filtrar por ID en lugar de código:
            # qs = qs.filter(tipo_item_id=tipo)

        # 2) Filtrar por búsqueda de texto en código o descripción
        q = self.request.query_params.get('q', None)
        if q:
            qs = qs.filter(
                Q(codigo__icontains=q) |
                Q(descripcion__icontains=q)
            )

        return qs
    
class ProductoDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()
    permission_classes = [IsAuthenticated]

# Crear un nuevo producto
class ProductoCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminOrSupervisor]

# Actualizar (editar) un producto existente
class ProductoUpdateAPIView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminOrSupervisor]

# Eliminar un producto
class ProductoDestroyAPIView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
#  TIPO TRIBUTOS
######################################################

# listar los tipos de tributos
class TiposTributosListAPIView(generics.ListAPIView):
    queryset = TipoTributo.objects.all()
    serializer_class = TiposTributosSerializer
    permission_classes = [IsAuthenticated]

class TributoByTipoListAPIView(generics.ListAPIView):
    serializer_class = TributosSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        tipo_tributo_id = self.kwargs['tipo_valor']
        return Tributo.objects.filter(tipo_valor=tipo_tributo_id)

# crear un nuevo tipo de tributo
class TiposTributosCreateAPIView(generics.CreateAPIView):
    queryset = TipoTributo.objects.all()
    serializer_class = TiposTributosSerializer
    permission_classes = [IsAdminOrSupervisor]

# Actualizar (editar) un tipo de tributo existente
class TiposTributosUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoTributo.objects.all()
    serializer_class = TiposTributosSerializer
    permission_classes = [IsAdminOrSupervisor]

# Eliminar un tipo de tributo
class TiposTributosDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoTributo.objects.all()
    serializer_class = TiposTributosSerializer
    permission_classes = [IsAdminOrSupervisor]


######################################################
# TRIBUTOS
######################################################

# listar todos los tributos
class TributosListAPIView(generics.ListAPIView):
    serializer_class = TributosSerializer
    queryset = Tributo.objects.all()
    permission_classes = [IsAuthenticated]

# listar detalle de tributo
class TributoDetailsAPIView(generics.RetrieveAPIView):
    queryset = Tributo.objects.all()
    serializer_class = TributosSerializer
    permission_classes = [IsAuthenticated]

# Crear un nuevo tributo
class TributoCreateAPIView(generics.CreateAPIView):
    serializer_class = TributosSerializer
    permission_classes = [IsAdminOrSupervisor]

# Actualizar (editar) un tributo existente
class TributoUpdateAPIView(generics.UpdateAPIView):
    queryset = Tributo.objects.all()
    serializer_class = TributosSerializer
    permission_classes = [IsAdminOrSupervisor]

# Eliminar un tributo
class TributoDestroyAPIView(generics.DestroyAPIView):
    queryset = Tributo.objects.all()
    serializer_class = TributosSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# UNIDAD DE MEDIDA
######################################################

# listar todos las unidades de medida
class UnidadMedidaListAPIView(generics.ListAPIView):
    queryset = TipoUnidadMedida.objects.all()
    serializer_class = TipoUnidadMedidaSerializer
    permission_classes = [IsAuthenticated]

# crear un nueva unidad de medida
class UnidadMedidaCreateAPIView(generics.CreateAPIView):
    queryset = TipoUnidadMedida.objects.all()
    serializer_class = TipoUnidadMedidaSerializer
    permission_classes = [IsAdminOrSupervisor]

# Actualizar (editar) una unidad de medida existente
class UnidadMedidaUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoUnidadMedida.objects.all()
    serializer_class = TipoUnidadMedidaSerializer
    permission_classes = [IsAdminOrSupervisor]

# Eliminar una unidad de medida
class UnidadMedidaDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoUnidadMedida.objects.all()
    serializer_class = TipoUnidadMedidaSerializer
    permission_classes = [IsAdminOrSupervisor]


######################################################
# TIPO ITEM
######################################################

# listar todos los tipos de item
class TipoItemListAPIView(generics.ListAPIView):
    queryset = TipoItem.objects.all()
    serializer_class = TipoItemSerializer
    permission_classes = [IsAuthenticated]

# crear un nuevo tipo de item
class TipoItemCreateAPIView(generics.CreateAPIView):
    queryset = TipoItem.objects.all()
    serializer_class = TipoItemSerializer
    permission_classes = [IsAdminOrSupervisor]

# Actualizar (editar) un tipo de item existente
class TipoItemUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoItem.objects.all()
    serializer_class = TipoItemSerializer
    permission_classes = [IsAdminOrSupervisor]

# Eliminar un tipo de item
class TipoItemDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoItem.objects.all()
    serializer_class = TipoItemSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# IMPUESTOS
######################################################

# listar todos los impuestos
class ImpuestosListAPIView(generics.ListAPIView):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer
    permission_classes = [IsAuthenticated]

# crear un nuevo impuesto
class ImpuestosCreateAPIView(generics.CreateAPIView):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer
    permission_classes = [IsAdminOrSupervisor]

# Actualizar (editar) un impuesto existente
class ImpuestosUpdateAPIView(generics.UpdateAPIView):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer
    permission_classes = [IsAdminOrSupervisor]

# Eliminar un impuesto
class ImpuestosDestroyAPIView(generics.DestroyAPIView):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# ALMACENES
######################################################

# listar todos los almacenes
class AlmacenesListAPIView(generics.ListAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    permission_classes = [IsAuthenticated]

class AlmacenesDetailAPIView(generics.RetrieveAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    permission_classes = [IsAuthenticated]

# crear un nuevo almacen
class AlmacenesCreateAPIView(generics.CreateAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    permission_classes = [IsAdminOrSupervisor]

# Actualizar (editar) un almacen existente
class AlmacenesUpdateAPIView(generics.UpdateAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    permission_classes = [IsAdminOrSupervisor]

# Eliminar un almacen
class AlmacenesDestroyAPIView(generics.DestroyAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
    permission_classes = [IsAdminOrSupervisor]


######################################################
# VISTAS PARA PROVEEDORES
######################################################
class ProveedorListAPIView(generics.ListAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class ProveedorCreateAPIView(generics.CreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAdminOrSupervisor]

class ProveedorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

class ProveedorUpdateAPIView(generics.UpdateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAdminOrSupervisor]

class ProveedorDestroyAPIView(generics.DestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAdminOrSupervisor]
    
######################################################
# VISTAS PARA PRODUCTOS DE SUJETO EXCLUIDO
######################################################
class ProductosProveedorListAPIView(generics.ListAPIView):
    queryset = ProductoProveedor.objects.all()
    serializer_class = ProductosProveedorSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class ProductosPorIdProveedorListAPIView(generics.ListAPIView):
    serializer_class = ProductosProveedorSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        provedor_id = self.kwargs['proveedor_id']
        return ProductoProveedor.objects.filter(proveedor__id=provedor_id)

class ProductoProveedorCreateAPIView(generics.CreateAPIView):
    queryset = ProductoProveedor.objects.all()
    serializer_class = ProductosProveedorSerializer
    permission_classes = [IsAdminOrSupervisor]

class ProductoProveedorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ProductoProveedor.objects.all()
    serializer_class = ProductosProveedorSerializer
    permission_classes = [IsAuthenticated]

class ProductoProveedorUpdateAPIView(generics.UpdateAPIView):
    queryset = ProductoProveedor.objects.all()
    serializer_class = ProductosProveedorSerializer
    permission_classes = [IsAdminOrSupervisor]

class ProductoProveedorDestroyAPIView(generics.DestroyAPIView):
    queryset = ProductoProveedor.objects.all()
    serializer_class = ProductosProveedorSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# VISTAS PARA COMPRAS
######################################################
class CompraListAPIView(generics.ListAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class CompraCreateAPIView(generics.CreateAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = [IsAdminOrSupervisor]

class CompraRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = [IsAuthenticated]

class CompraUpdateAPIView(generics.UpdateAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = [IsAdminOrSupervisor]

class CompraDestroyAPIView(generics.DestroyAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# VISTAS PARA DETALLE DE COMPRAS
######################################################
class DetalleCompraListAPIView(generics.ListAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [IsAuthenticated]

class DetalleCompraCreateAPIView(generics.CreateAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [IsAdminOrSupervisor]

class DetalleCompraRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [IsAuthenticated]

class DetallesPorCompraView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, compra_id):
        compra = get_object_or_404(Compra, id=compra_id)
        detalles = compra.detalles.all()
        serializer = DetalleCompraReadSerializer(detalles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetalleCompraUpdateAPIView(generics.UpdateAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [IsAdminOrSupervisor]

class DetalleCompraDestroyAPIView(generics.DestroyAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# VISTAS PARA MOVIMIENTOS DE INVENTARIO (KARDEX)
######################################################
class MovimientoInventarioListAPIView(generics.ListAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class MovimientoInventarioCreateAPIView(generics.CreateAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    permission_classes = [IsAdminOrSupervisor]

class MovimientoInventarioRetrieveAPIView(generics.RetrieveAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    permission_classes = [IsAuthenticated]

class MovimientoInventarioUpdateAPIView(generics.UpdateAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    permission_classes = [IsAdminOrSupervisor]

class MovimientoInventarioDestroyAPIView(generics.DestroyAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# VISTAS PARA AJUSTES DE INVENTARIO
######################################################
class AjusteInventarioListAPIView(generics.ListAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class AjusteInventarioCreateAPIView(generics.CreateAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer
    permission_classes = [IsAdminOrSupervisor]

class AjusteInventarioRetrieveAPIView(generics.RetrieveAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer
    permission_classes = [IsAuthenticated]

class AjusteInventarioUpdateAPIView(generics.UpdateAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer
    permission_classes = [IsAdminOrSupervisor]

class AjusteInventarioDestroyAPIView(generics.DestroyAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# VISTAS PARA DEVOLUCIONES DE VENTA
######################################################
class DevolucionVentaListAPIView(generics.ListAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class DevolucionVentaCreateAPIView(generics.CreateAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer
    permission_classes = [IsAdminOrSupervisor]

class DevolucionVentaRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer
    permission_classes = [IsAuthenticated]

class DevolucionVentaUpdateAPIView(generics.UpdateAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer
    permission_classes = [IsAdminOrSupervisor]

class DevolucionVentaDestroyAPIView(generics.DestroyAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# VISTAS PARA DETALLE DE DEVOLUCIONES DE VENTA
######################################################
class DetalleDevolucionVentaListAPIView(generics.ListAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer
    permission_classes = [IsAuthenticated]

class DetalleDevolucionVentaCreateAPIView(generics.CreateAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer
    permission_classes = [IsAdminOrSupervisor]

class DetalleDevolucionVentaRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer
    permission_classes = [IsAuthenticated]

class DetalleDevolucionVentaUpdateAPIView(generics.UpdateAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer
    permission_classes = [IsAdminOrSupervisor]

class DetalleDevolucionVentaDestroyAPIView(generics.DestroyAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# VISTAS PARA DEVOLUCIONES A PROVEEDORES
######################################################
class DevolucionCompraListAPIView(generics.ListAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class DevolucionCompraCreateAPIView(generics.CreateAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer
    permission_classes = [IsAdminOrSupervisor]

class DevolucionCompraRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer
    permission_classes = [IsAuthenticated]

class DevolucionCompraUpdateAPIView(generics.UpdateAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer
    permission_classes = [IsAdminOrSupervisor]

class DevolucionCompraDestroyAPIView(generics.DestroyAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer
    permission_classes = [IsAdminOrSupervisor]

######################################################
# VISTAS PARA DETALLES DE DEVOLUCIONES A PROVEEDORES
######################################################
class DetalleDevolucionCompraListAPIView(generics.ListAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer
    permission_classes = [IsAuthenticated]

class DetalleDevolucionCompraCreateAPIView(generics.CreateAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer
    permission_classes = [IsAdminOrSupervisor]

class DetalleDevolucionCompraRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer
    permission_classes = [IsAuthenticated]

class DetalleDevolucionCompraUpdateAPIView(generics.UpdateAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer
    permission_classes = [IsAdminOrSupervisor]

class DetalleDevolucionCompraDestroyAPIView(generics.DestroyAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer
    permission_classes = [IsAdminOrSupervisor]