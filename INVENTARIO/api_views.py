
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    AlmacenSerializer, ImpuestoSerializer, ProductoSerializer, TipoItemSerializer,
    TipoUnidadMedidaSerializer, TiposTributosSerializer, TributosSerializer, 
    ProveedorSerializer, CompraSerializer, DetalleCompraSerializer,
    MovimientoInventarioSerializer, AjusteInventarioSerializer,
    DevolucionVentaSerializer, DetalleDevolucionVentaSerializer,
    DevolucionCompraSerializer, DetalleDevolucionCompraSerializer
    )
from .models import (
    Almacen, Impuesto, Producto, TipoItem, TipoTributo, TipoUnidadMedida, Tributo,
    Proveedor, Compra, DetalleCompra, MovimientoInventario, AjusteInventario,
    DevolucionVenta, DetalleDevolucionVenta, DevolucionCompra, DetalleDevolucionCompra
    )
from django.db.models import Q

     
######################################################
# PRODUCTOS Y SERVICIOS
######################################################

# Listar productos con filtrado por código o descripción
class ProductoListAPIView(generics.ListAPIView):
    serializer_class = ProductoSerializer

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

# Crear un nuevo producto
class ProductoCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductoSerializer

# Actualizar (editar) un producto existente
class ProductoUpdateAPIView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Eliminar un producto
class ProductoDestroyAPIView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


######################################################
#  TIPO TRIBUTOS
######################################################

# listar los tipos de tributos
class TiposTributosListAPIView(generics.ListAPIView):
    queryset = TipoTributo.objects.all()
    serializer_class = TiposTributosSerializer
    
class TributoByTipoListAPIView(generics.ListAPIView):
    serializer_class = TributosSerializer
    
    def get_queryset(self):
        # Obtener el id del departamento de la URL
        tipo_tributo_id = self.kwargs['tipo_valor']
        # Filtrar los municipios por el departamento
        return Tributo.objects.filter(tipo_valor=tipo_tributo_id)

# crear un nuevo tipo de tributo
class TiposTributosCreateAPIView(generics.CreateAPIView):
    queryset = TipoTributo.objects.all()
    serializer_class = TiposTributosSerializer

# Actualizar (editar) un tipo de tributo existente
class TiposTributosUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoTributo.objects.all()
    serializer_class = TiposTributosSerializer

# Eliminar un tipo de tributo
class TiposTributosDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoTributo.objects.all()
    serializer_class = TiposTributosSerializer


######################################################
# TRIBUTOS
######################################################

# listar todos los tributos
class TributosListAPIView(generics.ListAPIView):
    serializer_class = TributosSerializer
    queryset = Tributo.objects.all()

# listar detallle de tributo
class TributoDetailsAPIView(generics.RetrieveAPIView):
    queryset = Tributo.objects.all()
    serializer_class = TributosSerializer

# Crear un nuevo tributo
class TributoCreateAPIView(generics.CreateAPIView):
    serializer_class = TributosSerializer

# Actualizar (editar) un tributo existente
class TributoUpdateAPIView(generics.UpdateAPIView):
    queryset = Tributo.objects.all()
    serializer_class = TributosSerializer

# Eliminar un tributo
class TributoDestroyAPIView(generics.DestroyAPIView):
    queryset = Tributo.objects.all()
    serializer_class = TributosSerializer

######################################################
# UNIDAD DE MEDIDA
######################################################

# listar todos las unidades de medida
class UnidadMedidaListAPIView(generics.ListAPIView):
    queryset = TipoUnidadMedida.objects.all()
    serializer_class = TipoUnidadMedidaSerializer

# crear un nueva unidad de medida
class UnidadMedidaCreateAPIView(generics.CreateAPIView):
    queryset = TipoUnidadMedida.objects.all()
    serializer_class = TipoUnidadMedidaSerializer

# Actualizar (editar) una unidad de medida existente
class UnidadMedidaUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoUnidadMedida.objects.all()
    serializer_class = TipoUnidadMedidaSerializer

# Eliminar una unidad de medida
class UnidadMedidaDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoUnidadMedida.objects.all()
    serializer_class = TipoUnidadMedidaSerializer


######################################################
# TIPO ITEM
######################################################

# listar todos los tipos de item
class TipoItemListAPIView(generics.ListAPIView):
    queryset = TipoItem.objects.all()
    serializer_class = TipoItemSerializer

# crear un nuevo tipo de item
class TipoItemCreateAPIView(generics.CreateAPIView):
    queryset = TipoItem.objects.all()
    serializer_class = TipoItemSerializer

# Actualizar (editar) un tipo de item existente
class TipoItemUpdateAPIView(generics.UpdateAPIView):
    queryset = TipoItem.objects.all()
    serializer_class = TipoItemSerializer

# Eliminar un tipo de item
class TipoItemDestroyAPIView(generics.DestroyAPIView):
    queryset = TipoItem.objects.all()
    serializer_class = TipoItemSerializer

######################################################
# IMPUESTOS
######################################################

#listar todos los impuestos
class ImpuestosListAPIView(generics.ListAPIView):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer

# crear un nuevo impuesto
class ImpuestosCreateAPIView(generics.CreateAPIView):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer

# Actualizar (editar) un impuesto existente
class ImpuestosUpdateAPIView(generics.UpdateAPIView):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer

# Eliminar un impuesto
class ImpuestosDestroyAPIView(generics.DestroyAPIView):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer

######################################################
# ALMACENES
######################################################

# listar todos los almacenes
class AlmacenesListAPIView(generics.ListAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer

# crear un nuevo almacen
class AlmacenesCreateAPIView(generics.CreateAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer

# Actualizar (editar) un almacen existente
class AlmacenesUpdateAPIView(generics.UpdateAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer

# Eliminar un almacen
class AlmacenesDestroyAPIView(generics.DestroyAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer


######################################################
# VISTAS PARA PROVEEDORES
######################################################
class ProveedorListAPIView(generics.ListAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProveedorCreateAPIView(generics.CreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProveedorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProveedorUpdateAPIView(generics.UpdateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProveedorDestroyAPIView(generics.DestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

######################################################
# VISTAS PARA COMPRAS
######################################################
class CompraListAPIView(generics.ListAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

class CompraCreateAPIView(generics.CreateAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

class CompraRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

class CompraUpdateAPIView(generics.UpdateAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

class CompraDestroyAPIView(generics.DestroyAPIView):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

######################################################
# VISTAS PARA DETALLE DE COMPRAS
######################################################
class DetalleCompraListAPIView(generics.ListAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer

class DetalleCompraCreateAPIView(generics.CreateAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer

class DetalleCompraRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer

class DetalleCompraUpdateAPIView(generics.UpdateAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer

class DetalleCompraDestroyAPIView(generics.DestroyAPIView):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer

######################################################
# VISTAS PARA MOVIMIENTOS DE INVENTARIO (KARDEX)
######################################################
class MovimientoInventarioListAPIView(generics.ListAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

class MovimientoInventarioCreateAPIView(generics.CreateAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

class MovimientoInventarioRetrieveAPIView(generics.RetrieveAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

class MovimientoInventarioUpdateAPIView(generics.UpdateAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

class MovimientoInventarioDestroyAPIView(generics.DestroyAPIView):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

######################################################
# VISTAS PARA AJUSTES DE INVENTARIO
######################################################
class AjusteInventarioListAPIView(generics.ListAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer

class AjusteInventarioCreateAPIView(generics.CreateAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer

class AjusteInventarioRetrieveAPIView(generics.RetrieveAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer

class AjusteInventarioUpdateAPIView(generics.UpdateAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer

class AjusteInventarioDestroyAPIView(generics.DestroyAPIView):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer

######################################################
# VISTAS PARA DEVOLUCIONES DE VENTA
######################################################
class DevolucionVentaListAPIView(generics.ListAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer

class DevolucionVentaCreateAPIView(generics.CreateAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer

class DevolucionVentaRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer

class DevolucionVentaUpdateAPIView(generics.UpdateAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer

class DevolucionVentaDestroyAPIView(generics.DestroyAPIView):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer

######################################################
# VISTAS PARA DETALLE DE DEVOLUCIONES DE VENTA
######################################################
class DetalleDevolucionVentaListAPIView(generics.ListAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer

class DetalleDevolucionVentaCreateAPIView(generics.CreateAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer

class DetalleDevolucionVentaRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer

class DetalleDevolucionVentaUpdateAPIView(generics.UpdateAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer

class DetalleDevolucionVentaDestroyAPIView(generics.DestroyAPIView):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer

######################################################
# VISTAS PARA DEVOLUCIONES A PROVEEDORES
######################################################
class DevolucionCompraListAPIView(generics.ListAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer

class DevolucionCompraCreateAPIView(generics.CreateAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer

class DevolucionCompraRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer

class DevolucionCompraUpdateAPIView(generics.UpdateAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer

class DevolucionCompraDestroyAPIView(generics.DestroyAPIView):
    queryset = DevolucionCompra.objects.all()
    serializer_class = DevolucionCompraSerializer

######################################################
# VISTAS PARA DETALLES DE DEVOLUCIONES A PROVEEDORES
######################################################
class DetalleDevolucionCompraListAPIView(generics.ListAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer

class DetalleDevolucionCompraCreateAPIView(generics.CreateAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer

class DetalleDevolucionCompraRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer

class DetalleDevolucionCompraUpdateAPIView(generics.UpdateAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer

class DetalleDevolucionCompraDestroyAPIView(generics.DestroyAPIView):
    queryset = DetalleDevolucionCompra.objects.all()
    serializer_class = DetalleDevolucionCompraSerializer