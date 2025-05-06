from decimal import Decimal
from rest_framework import serializers
from FE.models import Descuento
from .models import Almacen, Categoria, Impuesto, Producto, TipoItem, TipoTributo, TipoUnidadMedida, Tributo, Proveedor, Compra, DetalleCompra, MovimientoInventario, AjusteInventario, DevolucionCompra, DevolucionVenta, DetalleDevolucionCompra, DetalleDevolucionVenta


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

class DetalleCompraSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=50)
    descripcion = serializers.CharField(max_length=255)
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), allow_null=True, required=False
    )
    unidad_medida = serializers.PrimaryKeyRelatedField(
        queryset=TipoUnidadMedida.objects.all(), allow_null=True, required=False
    )
    preunitario = serializers.DecimalField(max_digits=5, decimal_places=2)
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=2)

    cantidad = serializers.IntegerField(min_value=1)
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)

class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True, write_only=True)

    class Meta:
        model = Compra
        fields = ['proveedor', 'estado', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        compra = Compra.objects.create(**validated_data)
        total = Decimal('0.00')

        for det in detalles_data:
            prod_data = {
                'codigo': det['codigo'],
                'descripcion': det['descripcion'],
                'categoria': det.get('categoria'),
                'unidad_medida': det.get('unidad_medida'),
                'preunitario': det['preunitario'],
                'precio_venta': det['precio_venta'],
            }
            producto, created = Producto.objects.get_or_create(
                codigo=prod_data['codigo'], defaults=prod_data
            )
            if not created:
                # Actualizar campos excepto precio_compra
                producto.descripcion = prod_data['descripcion']
                producto.categoria = prod_data['categoria']
                producto.unidad_medida = prod_data['unidad_medida']
                producto.preunitario = prod_data['preunitario']
                producto.precio_venta = prod_data['precio_venta']
                producto.save(update_fields=[
                    'descripcion', 'categoria',
                    'unidad_medida', 'preunitario', 'precio_venta'
                ])

            detalle = DetalleCompra.objects.create(
                compra=compra,
                producto=producto,
                cantidad=det['cantidad'],
                precio_unitario=det['precio_unitario']
            )
            total += detalle.subtotal

        compra.total = total
        compra.save(update_fields=['total'])
        return compra

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
