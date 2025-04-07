
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductoSerializer, TiposTributosSerializer, TributosSerializer
from .models import Producto, TipoTributo, Tributo

     
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

class TributoDetailsAPIView(generics.RetrieveAPIView):
    queryset = Tributo.objects.all()
    serializer_class = TributosSerializer