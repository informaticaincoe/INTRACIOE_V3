
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AlmacenSerializer, ImpuestoSerializer, ProductoSerializer, TipoItemSerializer, TipoUnidadMedidaSerializer, TiposTributosSerializer, TributosSerializer
from .models import Almacen, Impuesto, Producto, TipoItem, TipoTributo, TipoUnidadMedida, Tributo

     
######################################################
# PRODUCTOS Y SERVICIOS
######################################################

# Listar productos con filtrado por código o descripción
class ProductoListAPIView(generics.ListAPIView):
    serializer_class = ProductoSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        queryset = Producto.objects.all()
        if query:
            queryset = queryset.filter(Q(codigo__icontains=query) | Q(descripcion__icontains=query))
        return queryset
    
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

# class ProductoCreateAPIView(generics.CreateAPIView):
#     """
#     POST /api/productos/ → crea un Producto (incluye M2M e imagen)
#     """
#     queryset = Producto.objects.all()
#     serializer_class = ProductoSerializer
#     #para aceptar tanto JSON como multipart/form-data (imagen)


######################################################
# TRIBUTOS
######################################################

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

class TributosListAPIView(generics.ListAPIView):
    serializer_class = TributosSerializer
    queryset = Tributo.objects.all()

class TributoDetailsAPIView(generics.RetrieveAPIView):
    queryset = Tributo.objects.all()
    serializer_class = TributosSerializer

class UnidadMedidaListAPIView(generics.ListAPIView):
    queryset = TipoUnidadMedida.objects.all()
    serializer_class = TipoUnidadMedidaSerializer

class TipoItemListAPIView(generics.ListAPIView):
    queryset = TipoItem.objects.all()
    serializer_class = TipoItemSerializer

class ImpuestosListAPIView(generics.ListAPIView):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer

class AlmacenesListAPIView(generics.ListAPIView):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer
