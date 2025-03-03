from decimal import ROUND_HALF_UP, Decimal
from django.db import models
import uuid
from datetime import datetime

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
    descripcion = models.CharField(max_length=50)
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

class TipoItem(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Tipo_dte(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
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
        return f"{self.codigo} - {self.descripcion}"

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
    
class TipoUnidadMedida(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
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
    
#modelo para productos
class Producto(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    preunitario = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    tiene_descuento = models.BooleanField(default=False)
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

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

    def __str__(self):
        return self.nombre

class Emisor_fe(models.Model):
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT del Emisor")
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


    def __str__(self):
        return f"{self.nombre_razon_social} ({self.nit})"


# Modelo para manejar la numeración de control por año
class NumeroControl(models.Model):
    anio = models.IntegerField(unique=True)
    secuencia = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.anio} - {self.secuencia}"

    @staticmethod
    def obtener_numero_control():
        """
        Obtiene el número de control basado en el año y secuencia.
        """
        anio_actual = datetime.now().year
        control, creado = NumeroControl.objects.get_or_create(anio=anio_actual)
        numero_control = f"DTE-01-0000MOO1-{str(control.secuencia).zfill(15)}"
        control.secuencia += 1
        control.save()
        return numero_control

# Modelo de Factura Electrónica
class FacturaElectronica(models.Model):

    #IDENTIFICACION
    version = models.CharField(max_length=50)
    #ambiente = models.ForeignKey(Ambiente, on_delete=models.CASCADE, null=True)
    tipo_dte = models.ForeignKey(Tipo_dte, on_delete=models.CASCADE, null=True)
    numero_control = models.CharField(max_length=31, unique=True, blank=True)
    codigo_generacion = models.UUIDField(default=uuid.uuid4, unique=True)
    tipomodelo = models.ForeignKey(Modelofacturacion, on_delete=models.CASCADE, null=True)
    #tipooperacion = models.ForeignKey(CondicionOperacion, on_delete=models.CASCADE, null=True)
    tipocontingencia = models.ForeignKey(TipoContingencia, on_delete=models.CASCADE, null=True)
    motivocontin = models.CharField(max_length=350, null=True)
    fecha_emision = models.DateField(auto_now_add=True)
    hora_emision = models.TimeField(auto_now_add=True)
    tipomoneda = models.ForeignKey(TipoMoneda, on_delete=models.CASCADE, null=True)

    #EMISOR
    dteemisor = models.ForeignKey(Emisor_fe, on_delete=models.CASCADE, related_name='facturas_emisor_FE')
    
    #RECEPTOR
    dtereceptor = models.ForeignKey(Receptor_fe, on_delete=models.CASCADE, related_name='facturas_receptor_FE')
    
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

    #ESTADO DEL DOCUMENTO
    firmado = models.BooleanField(default=False)
    json_original = models.JSONField()
    json_firmado = models.JSONField(blank=True, null=True)
    sello_recepcion = models.CharField(max_length=255, blank=True, null=True)

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
    iva_item = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=Decimal('0.00'),)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2,help_text="Precio unitario del producto")
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0,help_text="Descuento aplicado (en monto) sobre el total sin IVA")
    ventas_no_sujetas = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ventas_exentas = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ventas_gravadas = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pre_sug_venta = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    no_gravado = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    #iva_item = models.DecimalField(max_digits=10, decimal_places=2, blank=True, editable=False,help_text="IVA calculado (por ejemplo, 13% sobre el total sin IVA)")
    
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