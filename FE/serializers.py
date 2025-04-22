from rest_framework import serializers

from .models import (
    INCOTERMS,
    Departamento,
    Descuento,
    EventoContingencia,
    FormasPago,
    LoteContingencia,
    OtrosDicumentosAsociado,
    Pais,
    Plazo,
    TipoContingencia,
    TipoDocContingencia,
    TipoDomicilioFiscal,
    TipoDonacion,
    TipoPersona,
    TipoRetencionIVAMH,
    TipoTransmision,
    TipoTransporte,
    TiposServicio_Medico,
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
    TipoGeneracionDocumento
)
from INVENTARIO.models import Producto, TipoItem, TipoTributo, Tributo

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

# Serializador para Emisor_fe
class EmisorSerializer(serializers.ModelSerializer):
    # Campo adicional para mostrar el codigo del tipo de establecimiento
    tipo_establecimiento_codigo = serializers.SerializerMethodField()

    class Meta:
        model = Emisor_fe
        fields = '__all__'  # Esto incluirá todos los campos del modelo y el campo adicional

    def get_tipo_establecimiento_codigo(self, obj):
        # Verificamos si el tipoestablecimiento existe y luego devolvemos el 'codigo'
        return obj.tipoestablecimiento.codigo if obj.tipoestablecimiento else None


class ReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receptor_fe
        fields = '__all__'


class FacturaListSerializer(serializers.ModelSerializer):
    estado_invalidacion = serializers.SerializerMethodField()

    class Meta:
        model = FacturaElectronica
        fields = [
            'id',
            'tipo_dte',
            'numero_control',
            'estado',  # Campo que ya existe en el modelo, p.ej. para indicar si está activa o inactiva.
            'codigo_generacion',
            'sello_recepcion',
            'fecha_emision',
            'total_pagar',
            'total_iva',
            'recibido_mh',
            'estado_invalidacion',  # Campo calculado a partir de dte_invalidacion.
        ]

    def get_estado_invalidacion(self, obj):
        evento = obj.dte_invalidacion.first()
        if evento:
            return "Invalidada" if evento.estado else "En proceso de invalidación"
        return "Viva"


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


##############################################################################
# SERIALIZER PARA CATALOGOS 
##############################################################################

class NumeroControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumeroControl
        fields = '__all__'

class TipoUnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUnidadMedida
        fields = '__all__'

class TipoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoItem
        fields = '__all__'

class TipoDteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_dte
        fields = '__all__'

class ActividadEconomicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadEconomica
        fields = '__all__'

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente
        fields = '__all__'

class ModelofacturacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelofacturacion
        fields = '__all__'

class TipoTransmisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTransmision
        fields = '__all__'

class TipoContingenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoContingencia
        fields = '__all__'

class TipoRetencionIVAMHSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoRetencionIVAMH
        fields = '__all__'

class TiposGeneracionDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoGeneracionDocumento
        fields = '__all__'

class TiposEstablecimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposEstablecimientos
        fields = '__all__'

class TiposServicio_MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposServicio_Medico
        fields = '__all__'

class OtrosDicumentosAsociadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtrosDicumentosAsociado
        fields = '__all__'

class TiposDocIDReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposDocIDReceptor
        fields = '__all__'

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

class CondicionOperacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CondicionOperacion
        fields = '__all__'

class FormasPagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormasPago
        fields = '__all__'

class PlazoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plazo
        fields = '__all__'

class TipoDocContingenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocContingencia
        fields = '__all__'

class TipoInvalidacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInvalidacion
        fields = '__all__'

class TipoDonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDonacion
        fields = '__all__'

class TipoPersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPersona
        fields = '__all__'

class TipoTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTransporte
        fields = '__all__'

class INCOTERMS_Serializer(serializers.ModelSerializer):
    class Meta:
        model = INCOTERMS
        fields = '__all__'

class TipoDomicilioFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDomicilioFiscal
        fields = '__all__'

class TipoMonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMoneda
        fields = '__all__'

class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = '__all__'


##############################################################################
# SERIALIZER PARA CONTINGENCIAS
##############################################################################

class LoteContingenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteContingencia
        fields = '__all__'

class EventoContingenciaSerializer(serializers.ModelSerializer):
    factura = FacturaElectronicaSerializer(many=True, read_only=True)
    lotes   = LoteContingenciaSerializer(source='lotes_evento', many=True, read_only=True)

    class Meta:
        model = EventoContingencia
        fields = [
            'id',
            'recibido_mh',
            'sello_recepcion',
            'factura',
            'lotes',
        ]