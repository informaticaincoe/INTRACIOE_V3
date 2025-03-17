from rest_framework import serializers

from rest_framework import serializers
from .models import (
    Departamento,
    Token_data,
    Ambiente,
    CondicionOperacion,
    DetalleFactura,
    FacturaElectronica,
    Modelofacturacion,
    NumeroControl,
    Emisor_fe,
    ActividadEconomica,
    Receptor_fe,
    Tipo_dte,
    TipoMoneda,
    TipoUnidadMedida,
    TiposDocIDReceptor,
    Municipio,
    EventoInvalidacion,
    TipoInvalidacion,
    TiposEstablecimientos,
)
from INVENTARIO.models import Producto, TipoItem

# Serializer para la autenticación vía API
class AuthRequestSerializer(serializers.Serializer):
    user = serializers.CharField(required=True)
    pwd = serializers.CharField(required=True)

class AuthResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    token = serializers.CharField()
    roles = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )

# Serializers basados en ModelSerializer para cada modelo

class ActividadEconomicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadEconomica
        fields = ['id', 'codigo', 'descripcion']

class EmisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emisor_fe
        fields = '__all__'

class ReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receptor_fe
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class TipoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoItem
        fields = '__all__'

class FacturaElectronicaSerializer(serializers.ModelSerializer):
    # Si deseas incluir los detalles de factura, podrías anidar el serializer
    detalles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = FacturaElectronica
        fields = '__all__'

class DetalleFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleFactura
        fields = '__all__'

class TokenDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token_data
        fields = '__all__'

class EventoInvalidacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoInvalidacion
        fields = '__all__'

# Serializers adicionales para otros modelos

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente
        fields = '__all__'

class CondicionOperacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicionOperacion
        fields = '__all__'

class ModelofacturacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelofacturacion
        fields = '__all__'

class NumeroControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumeroControl
        fields = '__all__'

class TipoDteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_dte
        fields = '__all__'

class TipoMonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMoneda
        fields = '__all__'

class TipoUnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUnidadMedida
        fields = '__all__'

class TiposDocIDReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposDocIDReceptor
        fields = '__all__'
        
class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'
class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

class TipoInvalidacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInvalidacion
        fields = '__all__'

class TiposEstablecimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposEstablecimientos
        fields = '__all__'
