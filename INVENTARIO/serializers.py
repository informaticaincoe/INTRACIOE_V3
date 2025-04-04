from rest_framework import serializers
from FE.models import Descuento
from .models import Producto, TipoItem, TipoTributo, Tributo


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class TipoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoItem
        fields = '__all__'

class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = '__all__'


class TiposTributosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTributo
        fields = '__all__'


class TributosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tributo
        fields = '__all__'
