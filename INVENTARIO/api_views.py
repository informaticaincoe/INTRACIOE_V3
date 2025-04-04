
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from INVENTARIO.serializers import ProductoSerializer, TiposTributosSerializer, TributosSerializer
from INVENTARIO.models import Producto, TipoTributo, Tributo

     
######################################################
# PRODUCTOS Y SERVICIOS
######################################################

class productosListAPIView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

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