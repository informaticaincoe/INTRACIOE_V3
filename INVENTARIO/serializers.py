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

class DetalleDevolucionVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleDevolucionVenta
        fields = '__all__'

class DevolucionVentaSerializer(serializers.ModelSerializer):
    detalles = DetalleDevolucionVentaSerializer(many=True, write_only=True)

    class Meta:
        model = DevolucionVenta
        # incluimos 'detalles' para escritura; los demás campos según tu modelo
        fields = ['num_factura', 'motivo', 'estado', 'usuario', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        # 1) Creamos la devolución
        devolucion = DevolucionVenta.objects.create(**validated_data)
        # 2) Creamos cada detalle con el motivo que venga del frontend
        for det in detalles_data:
            DetalleDevolucionVenta.objects.create(
                devolucion=devolucion,
                producto=det['producto'],
                cantidad=det['cantidad'],
                motivo_detalle=det['motivo_detalle']
            )
        return devolucion

class DetalleDevolucionCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleDevolucionCompra
        fields = '__all__'

class DevolucionCompraSerializer(serializers.ModelSerializer):
    detalles = DetalleDevolucionCompraSerializer(many=True, write_only=True)

    class Meta:
        model = DevolucionCompra
        # Incluimos 'detalles' para recepción en POST, pero no lo leemos en GET
        fields = ['compra', 'motivo', 'estado', 'usuario', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        # 1) Creamos la DevolucionCompra
        devolucion = DevolucionCompra.objects.create(**validated_data)
        # 2) Creamos automáticamente cada DetalleDevolucionCompra con el motivo que venga
        for det in detalles_data:
            DetalleDevolucionCompra.objects.create(
                devolucion=devolucion,
                producto=det['producto'],
                cantidad=det['cantidad'],
                motivo_detalle=det['motivo_detalle']
            )
        return devolucion
