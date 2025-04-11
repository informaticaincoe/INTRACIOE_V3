from rest_framework import serializers
from FE.models import Descuento
from .models import Almacen, Impuesto, Producto, TipoItem, TipoTributo, TipoUnidadMedida, Tributo, Proveedor, Compra, DetalleCompra, MovimientoInventario, AjusteInventario, DevolucionCompra, DevolucionVenta, DetalleDevolucionCompra, DetalleDevolucionVenta


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

class TipoUnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUnidadMedida
        fields = '__all__'

class ImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impuesto
        fields = '__all__'

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'
        read_only_fields = ['fecha']  # Fecha generada automáticamente

class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = '__all__'

class MovimientoInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'
        read_only_fields = ['fecha']

class AjusteInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AjusteInventario
        fields = '__all__'
        read_only_fields = ['fecha']

class DevolucionVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevolucionVenta
        fields = '__all__'
        read_only_fields = ['fecha']

class DetalleDevolucionVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleDevolucionVenta
        fields = '__all__'

class DevolucionCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevolucionCompra
        fields = '__all__'
        read_only_fields = ['fecha']

class DetalleDevolucionCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleDevolucionCompra
        fields = '__all__'