from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import ROUND_HALF_UP, Decimal
from INVENTARIO.models import Producto, ProductoProveedor, Proveedor, TipoItem, TipoUnidadMedida
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class ActividadEconomica(models.Model):
    codigo = models.CharField(max_length=50, verbose_name="Código de Actividad Económica")
    descripcion = models.TextField(verbose_name="Descripción")
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    class Meta:
        verbose_name = "actividad económica"
        verbose_name_plural = "actividades económicas"

class Ambiente(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return self.descripcion

class Modelofacturacion(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TipoTransmision(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TipoContingencia(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    #En el campo motivo_contingencia el contribuyente podra definir la razon de la contingencia, si el tipo de contingencia es 5, este campo sera obligatorio
    motivo_contingencia = models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TipoRetencionIVAMH(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TipoGeneracionDocumento(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TiposEstablecimientos(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TiposServicio_Medico(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

"""class TipoItem(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"""

class Tipo_dte(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    version = models.IntegerField(null=True, verbose_name=None)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion} - {self.version}"
    
class OtrosDicumentosAsociado(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class TiposDocIDReceptor(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class Pais(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Departamento(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Municipio(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class CondicionOperacion(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class FormasPago(models.Model):
    codigo = models.CharField( max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Plazo(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TipoDocContingencia(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class TipoInvalidacion(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        #return f"{self.codigo} - {self.descripcion}"
        return f"{self.codigo}"

class TipoDonacion(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class TipoPersona(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class TipoTransporte(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class INCOTERMS(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class TipoDomicilioFiscal(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class TipoMoneda(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class RecintoFiscal(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class RegimenExportacion(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
        
#modelo para descuentos por productos
class Descuento(models.Model):
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estdo = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.descripcion} - {self.porcentaje}%"

class Receptor_fe(models.Model):
    tipo_documento = models.ForeignKey(TiposDocIDReceptor, on_delete=models.CASCADE, null=True)
    num_documento = models.CharField(max_length=20, blank=True, null=True)
    nrc = models.CharField(max_length=8, blank=True, null=True)
    nombre = models.CharField(max_length=250)
    actividades_economicas = models.ManyToManyField(ActividadEconomica, verbose_name="Actividades Económicas")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    nombreComercial = models.CharField(max_length=150, null=True, verbose_name=None, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True)
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de Persona")

    #nuevos campos para georeferencia de cliente
    lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        validators=[MinValueValidator(Decimal("-90")), MaxValueValidator(Decimal("90"))],
        help_text="Latitud (WGS84)"
    )
    lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        validators=[MinValueValidator(Decimal("-180")), MaxValueValidator(Decimal("180"))],
        help_text="Longitud (WGS84)"
    )
    geocoded_at = models.DateTimeField(null=True, blank=True)
    geocode_source = models.CharField(max_length=30, blank=True, default="")

    def __str__(self):
        return self.nombre

class representanteEmisor(models.Model):
    nombre = models.CharField(max_length=200)
    tipo_documento = models.ForeignKey(TiposDocIDReceptor, on_delete=models.CASCADE, null=True)
    numero_documento = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.numero_documento})"
    
class Emisor_fe(models.Model):
    nit = models.CharField(max_length=20, verbose_name="NIT del Emisor")
    nrc = models.CharField(max_length=50, null=True)
    nombre_razon_social = models.CharField(max_length=255, verbose_name="Nombre o Razón Social")
    actividades_economicas = models.ManyToManyField(ActividadEconomica, verbose_name="Actividades Económicas")
    tipoestablecimiento = models.ForeignKey(TiposEstablecimientos, on_delete=models.CASCADE, null=True)
    nombre_comercial = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nombre Comercial")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True)
    direccion_comercial = models.TextField(verbose_name="Dirección Comercial")
    telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono")
    email = models.EmailField(null=True, blank=True, verbose_name="Correo Electrónico")
    codigo_establecimiento = models.CharField(max_length=10, null=True, blank=True, verbose_name="Código de Establecimiento")
    codigo_punto_venta = models.CharField(max_length=50, blank=True, verbose_name="Codigo de Punto de Venta", null=True)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE)
    nombre_establecimiento = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nombre Establecimiento")
    tipo_documento = models.ForeignKey(TiposDocIDReceptor, on_delete=models.CASCADE, null=True)
    logo = models.ImageField(upload_to='media/productos/', null=True, blank=True) #logo empresa
    clave_privada = models.CharField(max_length=255, null=True, blank=True)
    clave_publica = models.CharField(max_length=255, null=True, blank=True)
    representante = models.ForeignKey(representanteEmisor, on_delete=models.CASCADE, null=True, blank=True)
    tipoContribuyente = models.CharField(
        max_length=40,
        choices=[
            ('Gran Contribuyente', 'Gran Contribuyente'),
            ('Mediano Contribuyente', 'Mediano Contribuyente'),
            ('Pequeño Contribuyente', 'Pequeño Contribuyente'),
            ('Emprendedor', 'Emprendedor')
        ],
        default='Pequeño Contribuyente'
    )
    imprime_termica = models.BooleanField(
        default=False,
        verbose_name="Imprimir en térmica (80mm)"
    )
    
    
    def __str__(self):
        return f"{self.nombre_razon_social} ({self.nit})"

# Modelo para manejar la numeración de control por año

class NumeroControl(models.Model):
    codigo_establecimiento = models.CharField(max_length=4, null=True, blank=True, default="0000")
    codigo_punto_venta = models.CharField(max_length=4, null=True, blank=True, default="0001")
    anio = models.IntegerField()
    secuencia = models.IntegerField(default=1)
    tipo_dte = models.CharField(max_length=2, default="00", editable=True)

    class Meta:
        unique_together = (('anio', 'tipo_dte'),)

    def __str__(self):
        return f"{self.anio} - {self.secuencia} - {self.tipo_dte}"

    @staticmethod
    def obtener_numero_control(cod_dte, estab="0000", pv="0001"):
        print("Inicio asignar numero de control")
        anio_actual = datetime.now().year
        control, _ = NumeroControl.objects.get_or_create(anio=anio_actual, tipo_dte=cod_dte)

        # normalizar estab/pv
        estab = str(estab or "0000").zfill(4)
        pv = str(pv or "0001").zfill(4)
        secuencia = str(control.secuencia).zfill(15)

        # formato Hacienda: DTE-{tipo}-{estab}{pv}-{secuencia}
        numero_control = f"DTE-{cod_dte}-{estab}{pv}-{secuencia}"

        control.secuencia += 1
        control.save()

        print("Asignar numero de control:", numero_control, "len=", len(numero_control))
        return numero_control


    @staticmethod
    def preview_numero_control(cod_dte, estab="0000", pv="0001"):
        """
        Genera un número de control de vista previa sin incrementar la secuencia.
        """
        anio_actual = datetime.now().year
        current_sequence = 1
        try:
            control = NumeroControl.objects.get(anio=anio_actual, tipo_dte=cod_dte)
            current_sequence = control.secuencia
        except NumeroControl.DoesNotExist:
            pass

        return (
            f"DTE-{cod_dte}-"
            f"{str(estab).zfill(4)}{str(pv).zfill(4)}-"
            f"{str(current_sequence).zfill(15)}"
        )


# Modelo de Factura Electrónica
class FacturaElectronica(models.Model):
    #USUARIO QUE CREA EL DOCUMENTO
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    #IDENTIFICACION
    version = models.CharField(max_length=50)
    #ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE, null=True)
    tipo_dte = models.ForeignKey(Tipo_dte, on_delete=models.CASCADE, null=True)
    numero_control = models.CharField(max_length=31, unique=True, blank=True)
    codigo_generacion = models.UUIDField(default=uuid.uuid4, unique=True)
    tipomodelo = models.ForeignKey(Modelofacturacion, on_delete=models.CASCADE, null=True)
    #tipooperacion = models.ForeignKey(CondicionOperacion, on_delete=models.CASCADE, null=True)
    tipocontingencia = models.ForeignKey(TipoContingencia, on_delete=models.CASCADE, null=True, blank=True)
    motivocontin = models.CharField(max_length=350, null=True, blank=True)
    fecha_emision = models.DateField(auto_now_add=True) 
    hora_emision = models.TimeField(auto_now_add=True) 
    tipomoneda = models.ForeignKey(TipoMoneda, on_delete=models.CASCADE, null=True)

    #EMISOR
    dteemisor = models.ForeignKey(Emisor_fe, on_delete=models.CASCADE, related_name='facturas_emisor_FE')
    
    #RECEPTOR
    dtereceptor = models.ForeignKey(Receptor_fe, on_delete=models.CASCADE, related_name='facturas_receptor_FE')
    
    #CONTINGENCIA
    #dtecontingencia = models.ForeignKey(EventoContingencia, on_delete=models.CASCADE, related_name='contingencia_dte', null=True, blank=True)
    
    #RESUMEN
    total_no_sujetas = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_exentas = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_gravadas = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sub_total_ventas = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    descuen_no_sujeto = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    descuento_exento = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    descuento_gravado = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    por_descuento = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_descuento = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    iva_retenido = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    retencion_renta = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_operaciones = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_no_gravado = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_letras = models.CharField(max_length=250,null=True)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    condicion_operacion = models.ForeignKey(CondicionOperacion, on_delete=models.CASCADE, null=True)
    iva_percibido = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    saldo_favor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    formas_Pago = models.JSONField(blank=True, null=True)

    #ESTADO DEL DOCUMENTO
    firmado = models.BooleanField(default=False)
    json_original = models.JSONField()
    json_firmado = models.JSONField(blank=True, null=True)
    sello_recepcion = models.CharField(max_length=255, blank=True, null=True)
    recibido_mh = models.BooleanField(default=False)
    estado = models.BooleanField(default=False)
    contingencia = models.BooleanField(default=False)
    contingencia_recibida_mh = models.BooleanField(default=False)
    #tipo_documento_relacionar = models.CharField(max_length=50, null=True, blank=True)#Identificar si el documento es Fisico(F) o Electronico(E)
    #documento_relacionado = models.CharField(max_length=100, null=True, blank=True)#Agregar el documento relacionado
    base_imponible = models.BooleanField(default=False)
    tipotransmision = models.ForeignKey(TipoTransmision, on_delete=models.CASCADE, null=True, blank=True)
    
    fecha_modificacion = models.DateField(auto_now_add=True, null=True)
    hora_modificacion = models.TimeField(auto_now_add=True, null=True)
    
    envio_correo = models.BooleanField(default=False)
    envio_correo_contingencia = models.BooleanField(default=False)
    
    #EXPORTACION
    tipoItemEmisor = models.ForeignKey(TipoItem, on_delete=models.CASCADE, null=True)
    recintoFiscal = models.ForeignKey(RecintoFiscal, on_delete=models.CASCADE, null=True)
    regimenExportacion = models.ForeignKey(RegimenExportacion, on_delete=models.CASCADE, null=True)
    seguro_exportacion = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    flete_exportacion = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    incoterms = models.ForeignKey(INCOTERMS, on_delete=models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_control:
            super().save(*args, **kwargs)
            self.numero_control = f"DTE-01-{uuid.uuid4().hex[:8].upper()}-{str(self.pk).zfill(15)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.numero_control}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(FacturaElectronica, on_delete=models.CASCADE, related_name='detalles', help_text="Factura a la que pertenece este detalle")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,help_text="Producto asociado a este detalle")
    cantidad = models.PositiveIntegerField(default=1,help_text="Cantidad del producto")
    unidad_medida = models.ForeignKey(TipoUnidadMedida, on_delete=models.CASCADE, null=True)
    iva_item = models.DecimalField(max_digits=10, decimal_places=6, null=True, default=Decimal('0.00'),)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=6,help_text="Precio unitario del producto")
    #descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0,help_text="Descuento aplicado (en monto) sobre el total sin IVA")
    ventas_no_sujetas = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    ventas_exentas = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    ventas_gravadas = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    pre_sug_venta = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    no_gravado = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    tiene_descuento = models.BooleanField(default=False)
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, null=True, blank=True)
    #iva_item = models.DecimalField(max_digits=10, decimal_places=2, blank=True, editable=False,help_text="IVA calculado (por ejemplo, 13% sobre el total sin IVA)")
    saldo_favor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tipo_documento_relacionar = models.CharField(max_length=50, null=True, blank=True)#Identificar si el documento es Fisico(F) o Electronico(E)
    documento_relacionado = models.CharField(max_length=100, null=True, blank=True)#Agregar el documento relacionado
    # def save(self, *args, **kwargs):
    #     # Calcular el total sin IVA
    #     self.total_sin_iva = (self.cantidad * self.precio_unitario) - self.descuento
    #     # Calcular el IVA (con tasa del 13%) y redondearlo a dos decimales
    #     self.iva = (self.total_sin_iva * Decimal('0.13')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    #     # Calcular el total con IVA
    #     self.total_con_iva = self.total_sin_iva + self.iva
    #     # Asignar el IVA calculado al campo que se usará en el JSON
    #     self.iva_item = self.iva
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.factura.numero_control} - {self.producto.descripcion} ({self.cantidad} x {self.precio_unitario})"

# Modelo de Factura Sujeto excluido
class FacturaSujetoExcluidoElectronica(models.Model):
    #IDENTIFICACION
    version = models.CharField(max_length=50)
    #ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE, null=True)
    tipo_dte = models.ForeignKey(Tipo_dte, on_delete=models.CASCADE, null=True)
    numero_control = models.CharField(max_length=31, unique=True, blank=True)
    codigo_generacion = models.UUIDField(default=uuid.uuid4, unique=True)
    tipomodelo = models.ForeignKey(Modelofacturacion, on_delete=models.CASCADE, null=True)
    #tipooperacion = models.ForeignKey(CondicionOperacion, on_delete=models.CASCADE, null=True)
    tipocontingencia = models.ForeignKey(TipoContingencia, on_delete=models.CASCADE, null=True, blank=True)
    motivocontin = models.CharField(max_length=350, null=True, blank=True)
    fecha_emision = models.DateField(auto_now_add=True) 
    hora_emision = models.TimeField(auto_now_add=True) 
    tipomoneda = models.ForeignKey(TipoMoneda, on_delete=models.CASCADE, null=True)
    
    #EMISOR
    dteemisor = models.ForeignKey(Emisor_fe, on_delete=models.CASCADE, related_name='facturas_emisor_sujeto_excluido_FE')
    #SUJETO EXCLUIDO
    dtesujetoexcluido = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='facturas_sujeto_excluido_FE')
    
    #CONTINGENCIA
    #dtecontingencia = models.ForeignKey(EventoContingencia, on_delete=models.CASCADE, related_name='contingencia_dte', null=True, blank=True)
    
    #RESUMEN
    descuento = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_descuento = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    iva_retenido = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    retencion_renta = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_operaciones = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # total_no_gravado = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_letras = models.CharField(max_length=250,null=True)
    # total_iva = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    condicion_operacion = models.ForeignKey(CondicionOperacion, on_delete=models.CASCADE, null=True)
    # iva_percibido = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # saldo_favor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    formas_Pago = models.JSONField(blank=True, null=True)

    #ESTADO DEL DOCUMENTO
    firmado = models.BooleanField(default=False)
    json_original = models.JSONField()
    json_firmado = models.JSONField(blank=True, null=True)
    sello_recepcion = models.CharField(max_length=255, blank=True, null=True)
    recibido_mh = models.BooleanField(default=False)
    estado = models.BooleanField(default=False)
    contingencia = models.BooleanField(default=False)
    contingencia_recibida_mh = models.BooleanField(default=False)
    tipotransmision = models.ForeignKey(TipoTransmision, on_delete=models.CASCADE, null=True, blank=True)
    
    fecha_modificacion = models.DateField(auto_now_add=True, null=True)
    hora_modificacion = models.TimeField(auto_now_add=True, null=True)
    
    envio_correo = models.BooleanField(default=False)
    envio_correo_contingencia = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.numero_control:
            super().save(*args, **kwargs)
            self.numero_control = f"DTE-01-{uuid.uuid4().hex[:8].upper()}-{str(self.pk).zfill(15)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.numero_control}"

class DetalleFacturaSujetoExcluido(models.Model):
    factura = models.ForeignKey(FacturaSujetoExcluidoElectronica, on_delete=models.CASCADE, related_name='detallesSujetoExcluido', help_text="Factura a la que pertenece este detalle")
    producto = models.ForeignKey(ProductoProveedor, on_delete=models.CASCADE,help_text="Producto de sujeto exclusivo asociado a este detalle")
    cantidad = models.PositiveIntegerField(default=1,help_text="Cantidad del producto")
    unidad_medida = models.ForeignKey(TipoUnidadMedida, on_delete=models.CASCADE, null=True)
    tipo_item = models.CharField(max_length=150, null=True, blank=True)
    codigo = models.ForeignKey(TipoItem, on_delete=models.CASCADE, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=6,help_text="Precio unitario del producto")

    tiene_descuento = models.BooleanField(default=False)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), help_text="Porcentaje de descuento aplicado a esta línea")
   
    def __str__(self):
        return f"Factura {self.factura.numero_control} - {self.descripcion} ({self.cantidad} x {self.precio_unitario})"
    
class EventoInvalidacion(models.Model):    
    #Identificacion
    #si una factura esta relacionada indica que tiene un evento de invalidacion
    factura = models.ForeignKey(FacturaElectronica, blank=True, null=True, on_delete=models.CASCADE, related_name='dte_invalidacion', help_text="Evento de invalidacion a la que pertenece la Factura")
    facturaSujetoExcluido = models.ForeignKey(FacturaSujetoExcluidoElectronica,  blank=True, null=True, on_delete=models.CASCADE, related_name='dte_invalidacion_sujeto_excluido', help_text="Evento de invalidacion solo para sujeto exclusivo")
    codigo_generacion = models.UUIDField(default=uuid.uuid4, unique=True)
    fecha_anulacion = models.DateField(auto_now_add=True, null=True)
    hora_anulacion = models.TimeField(auto_now_add=True, null=True)

    #Documento
    #campo tipoDte, codigoGeneracion. selloHacienda, numeroControl y fechaEmision esta relacionado con la factura
    codigo_generacion_r = models.CharField(max_length=50, blank=True, null=True)
    #-Receptor: llena los campos tipoDocumento, numDocumento, nombre, telefono y correo [Acceder desde factura]
    #-dtereceptor = models.ForeignKey(Receptor_fe, on_delete=models.CASCADE, related_name='dte_invalidar_receptor_FE')

    #Motivo (tabla TipoInvalidacion)
    tipo_invalidacion = models.ForeignKey(TipoInvalidacion, on_delete=models.CASCADE, related_name='dte_tipo_invalidacion_FE')
    motivo_anulacion = models.CharField(max_length=255, blank=True, null=True)
    
    #Llena los campos nombreResponsable, tipoDocResponsable y numDocResponsable [Acceder desde factura]
    #dteemisor = models.ForeignKey(Emisor_fe, on_delete=models.CASCADE, related_name='dte_invalidacion_emisor_FE')
    
    nombre_solicita = models.CharField(max_length=255, verbose_name="Nombre o Razón Social", null=True) #Nombre de quien solicita la invalidacion, ya sea el receptor o emisor
    tipo_documento_solicita = models.CharField(max_length=20, blank=True, null=True) #Tipo de documento de quien solicita la invalidacion, ya sea el receptor o emisor
    numero_documento_solicita = models.CharField(max_length=20, blank=True, null=True) #Numero de doc de quien solicita la invalidacion, ya sea el receptor o emisor
    solicita_invalidacion = models.CharField(max_length=15, blank=True, null=True) #Especificar quien invalidara el dte. si el emisor o receptor
    json_invalidacion = models.JSONField(blank=True, null=True)
    json_firmado = models.JSONField(blank=True, null=True)
    firmado = models.BooleanField(default=False)
    sello_recepcion = models.CharField(max_length=255, blank=True, null=True)
    recibido_mh = models.BooleanField(default=False)
    estado = models.BooleanField(default=False)

class Token_data(models.Model):
    nit_empresa = models.CharField(max_length=20, unique=True)  # NIT de la empresa
    password_hacienda = models.CharField(max_length=255)  # Contraseña en texto plano
    password_privado = models.CharField(max_length=255, default="1")
    token = models.CharField(max_length=500, blank=True, null=True)
    token_type = models.CharField(max_length=255, default='Bearer')
    roles = models.JSONField(default=list)  # Almacena los roles como una lista JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # #nuevos campos
    activado = models.BooleanField(default=False, null=True) # Indica si el token ha sido activado
    fecha_caducidad = models.DateTimeField(default=timezone.now, null=True) # Fecha de expiración del token
    def __str__(self):
        return f"Token Data para {self.nit_empresa}"
    
    def save(self, *args, **kwargs):
        # Si es un nuevo registro, calcula la fecha de caducidad
        if not self.pk:
            self.fecha_caducidad = timezone.now() + timedelta(days=1)  # 24 horas

        # Desactivar el token anterior de la empresa
        Token_data.objects.filter(nit_empresa=self.nit_empresa, activado=True).update(activado=False)

        # Asegurar que el nuevo token se guarde como activado
        self.activado = True  

        super(Token_data, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Token Data"
        verbose_name_plural = "Token Data"
        
class EventoContingencia(models.Model):
    #Identificacion
    codigo_generacion = models.UUIDField(default=uuid.uuid4, unique=True)
    sello_recepcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_transmision = models.DateField(auto_now_add=True, null=True) #fInicio
    hora_transmision = models.TimeField(auto_now_add=True, null=True) #hInicio
    fecha_modificacion = models.DateField(auto_now_add=True, null=True)
    hora_modificacion = models.TimeField(auto_now_add=True, null=True)
    #lotecontingencia = models.ForeignKey(LoteContingencia, on_delete=models.CASCADE, null=True, blank=True, related_name="lotes_evento")
    tipo_contingencia = models.ForeignKey(TipoContingencia, on_delete=models.CASCADE, null=True)
    firmado = models.BooleanField(default=False)
    json_original = models.JSONField(blank=True, null=True)
    json_firmado = models.JSONField(blank=True, null=True)
    recibido_mh = models.BooleanField(default=False)
    #Agregar campos de fecha y hora que proporcionara hacienda
    f_fin = models.DateField(auto_now_add=True, null=True)
    h_fin = models.TimeField(auto_now_add=True, null=True)
    finalizado = models.BooleanField(default=False)
    #Si el evento fue rechazado se indicara el error para su correcion en un plazo máximo de 24 horas despues de haber sido rechazado
    rechazado = models.BooleanField(default=False) #manejar estado de envio de contingencia a MH
    observaciones = models.CharField(max_length=3000, blank=True, null=True)
    fecha_sello_recibido = models.DateTimeField(null=True, blank=True) 
    cantidad_lote = models.IntegerField(null=True, verbose_name=None)
    motivo_contingencia = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f"Contingencia {self.codigo_generacion} - {self.fecha_transmision} - {self.hora_transmision}"

class LoteContingencia(models.Model):
    #eventocontingencia = models.ForeignKey(EventoContingencia, on_delete=models.CASCADE, null=True, blank=True)
    recibido_mh = models.BooleanField(default=False)
    #estado = models.BooleanField(default=False)
    #cantidad_lote = models.IntegerField(null=True, verbose_name=None)
    evento = models.ForeignKey(
        EventoContingencia,
        related_name='lotes_contingencia',  # queda claro que son lotes de contingencia
        on_delete=models.CASCADE, null=True, blank=True
    )
    factura = models.ForeignKey(
        FacturaElectronica,
        related_name='lotes_de_factura',      # lotes en los que aparece esta factura
        on_delete=models.CASCADE, null=True, blank=True
    )
    finalizado = models.BooleanField(default=False)
    
    #Auditoria
    fecha_transmicion = models.DateField(auto_now_add=True, null=True) #fInicio
    hora_transmision = models.TimeField(auto_now_add=True, null=True)
    fecha_modificacion = models.DateField(auto_now_add=True, null=True)
    hora_modificacion = models.TimeField(auto_now_add=True, null=True)
    #evento = models.ForeignKey(EventoContingencia, related_name='lotecontingencia', on_delete=models.CASCADE)
    
