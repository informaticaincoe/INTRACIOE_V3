from decimal import Decimal
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    abreviatura = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"
    
class TipoUnidadMedida(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Impuesto(models.Model):
    nombre = models.CharField(max_length=50)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)  # Ejemplo: 13.00 para IVA

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"
    
# MODELO PARA ALMACENES
class Almacen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    responsable = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
#modelo para descuentos por productos
# class Descuento(models.Model):
#     porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
#     descripcion = models.CharField(max_length=50)
#     fecha_inicio = models.DateField()
#     fecha_fin = models.DateField()
#     estdo = models.BooleanField(default=True)
#     def __str__(self):
#         return f"{self.descripcion} - {self.porcentaje}%"
    
class TipoItem(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TipoTributo(models.Model):
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class TipoValor(models.Model):
    descripcion = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.descripcion}"

class Tributo(models.Model):
    tipo_tributo = models.ForeignKey(TipoTributo, on_delete=models.SET_NULL, null=True, blank=True)
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    valor_tributo = models.CharField(max_length=100, null=True)#models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tipo_valor = models.ForeignKey(TipoValor, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)  # SKU único
    descripcion = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    unidad_medida = models.ForeignKey(TipoUnidadMedida, on_delete=models.SET_NULL, null=True, blank=True)
    preunitario = models.DecimalField(max_digits=5, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    stock_maximo = models.PositiveIntegerField(default=0)
    
    impuestos = models.ManyToManyField(Impuesto, blank=True)  # Soporte para múltiples impuestos
    # tiene_descuento = models.BooleanField(default=False)
    # descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.SET_NULL, null=True, blank=True)
    referencia_interna = models.CharField(max_length=50, null=True, editable=True, default=None)
    tributo = models.ForeignKey(Tributo, on_delete=models.CASCADE, null=False, default=1)
    precio_iva = models.BooleanField(default=False) #Indicar si el producto se guarda con IVA
    
    # Control de lotes y vencimientos (Opcional)
    maneja_lotes = models.BooleanField(default=False)
    fecha_vencimiento = models.DateField(null=True, blank=True)  
    
    # Manejo de almacenes (Opcional)
    almacenes = models.ManyToManyField(Almacen, blank=True)

    # Imagen del producto (Opcional)
    imagen = models.ImageField(upload_to='media/productos/', null=True, blank=True)

    # Auditoría
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

# MODELO PARA PROVEEDORES
class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    num_documento = models.CharField(max_length=50, unique=True)
    tipo_documento = models.ForeignKey(
        "FE.TiposDocIDReceptor",       # <-- app_label.ModelName en lugar de import
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="DUI, NIT, etc."
    )
    actividades_economicas = models.ManyToManyField(
        "FE.ActividadEconomica",
        blank=True,
    )
    departamento = models.ForeignKey(
        "FE.Departamento",  # Modelo que contiene los departamentos
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Departamento del proveedor"
    )
    municipio = models.ForeignKey(
        "FE.Municipio",  # Modelo que contiene los municipios
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Municipio del proveedor"
    )


    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    condiciones_pago = models.CharField(max_length=100, blank=True, null=True)
    
    #pais: si es extranjero se aplica 20% de retención

    def __str__(self):
        return f"{self.nombre} - {self.num_documento}"

class ProductoProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='proveedor')
    codigo = models.CharField(max_length=50, unique=True)  # SKU único
    descripcion = models.CharField(max_length=255)
    unidad_medida = models.ForeignKey(TipoUnidadMedida, on_delete=models.SET_NULL, null=True, blank=True)
    preunitario = models.DecimalField(max_digits=5, decimal_places=2)
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.SET_NULL, null=True, blank=True)
    referencia_interna = models.CharField(max_length=50, null=True, editable=True, default=None)
    fecha_vencimiento = models.DateField(null=True, blank=True)  
    # Imagen del producto (Opcional)
    imagen = models.ImageField(upload_to='media/productos/', null=True, blank=True)

    # Auditoría
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    #impuestos = models.ManyToManyField(Impuesto, blank=True)  # Soporte para múltiples impuestos
    # tiene_descuento = models.BooleanField(default=False)
    # descuento = models.ForeignKey(Descuento, on_delete=models.SET_NULL, null=True, blank=True)
    
    #tributo = models.ForeignKey(Tributo, on_delete=models.CASCADE, null=False, default=1)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


# MODELO PARA COMPRAS
class Compra(models.Model):
    ESTADOS = [
        ('Pendiente','Pendiente'),
        ('Pagado','Pagado'),
        ('Devuelto','Devuelto'),     # <- NUEVO
        ('Cancelado','Cancelado'),
    ]
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    # Nuevos campos para Anexo de Compras
    tipo_documento = models.CharField(max_length=10, blank=True, null=True)
    numero_documento = models.CharField(max_length=100, blank=True, null=True)
    tipo_operacion = models.CharField(max_length=10, blank=True, null=True)
    clasificacion = models.CharField(max_length=10, blank=True, null=True)
    sector = models.CharField(max_length=10, blank=True, null=True)
    tipo_costo_gasto = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Compra {self.id} - {self.proveedor.nombre}"


# MODELO PARA DETALLE DE COMPRAS (PRODUCTOS COMPRADOS)
class DetalleCompra(models.Model):
    TIPO_COMPRA_CHOICES = [
        ('EX_INT','Interna Exenta'),
        ('EX_INT_NO','Internaciones Exentas/No Sujetas'),
        ('EX_IMP','Importaciones Exentas/No Sujetas'),
        ('GR_INT','Interna Gravada'),
        ('GR_INT_B','Internaciones Grav. Bienes'),
        ('GR_IMP_B','Importaciones Grav. Bienes'),
        ('GR_IMP_S','Importaciones Grav. Servicios'),
    ]

    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    # Nuevo campo para tipo de compra
    tipo_compra = models.CharField(
        max_length=12,
        choices=TIPO_COMPRA_CHOICES,
        default='GR_INT'
    )
    # Nuevo campo IVA calculado para el detalle
    iva_item = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        # calcular IVA si aplica
        if self.tipo_compra.startswith('GR'):
            self.iva_item = (self.subtotal * Decimal('0.13')).quantize(Decimal('0.01'))
        else:
            self.iva_item = Decimal('0.00')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.descripcion} - Compra {self.compra.id}"

# MODELO PARA MOVIMIENTOS DE INVENTARIO (KARDEX)
class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
        ('Ajuste', 'Ajuste'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    referencia = models.CharField(max_length=255, blank=True, null=True)  # Ejemplo: "Venta #123", "Compra #456"

    def __str__(self):
        return f"{self.tipo} - {self.cantidad} {self.producto.descripcion} ({self.almacen.nombre})"


# MODELO PARA AJUSTES DE INVENTARIO
class AjusteInventario(models.Model):
    movimiento = models.ForeignKey(MovimientoInventario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    cantidad_ajustada = models.IntegerField()  # Puede ser positivo o negativo
    motivo = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)  # Quién hizo el ajuste

    def __str__(self):
        return f"Ajuste {self.cantidad_ajustada} {self.producto.descripcion} ({self.almacen.nombre})"

# MODELO PARA DEVOLUCIONES DE CLIENTES (POST-VENTA)
class DevolucionVenta(models.Model):
    #venta = models.ForeignKey('Venta', on_delete=models.CASCADE, related_name='devoluciones')
    num_factura = models.CharField(max_length=150, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada')],
        default='Pendiente'
    )
    usuario = models.CharField(max_length=100, blank=True, null=True)  # Quién procesa la devolución

    def __str__(self):
        return f"Devolución {self.id} - {self.estado}"


# MODELO PARA DETALLES DE DEVOLUCIONES DE VENTAS
class DetalleDevolucionVenta(models.Model):
    devolucion = models.ForeignKey(DevolucionVenta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    motivo_detalle = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.descripcion} - Devolución {self.devolucion.id}"

#########################################################################################
# *** POR EL MOMENTO NO SE USA ***
# MODELO PARA NOTAS DE CRÉDITO (ASOCIADAS A DEVOLUCIONES DE VENTAS) 
class NotaCredito(models.Model):
    devolucion = models.ForeignKey(DevolucionVenta, on_delete=models.CASCADE, related_name="nota_credito")
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Emitida', 'Emitida'), ('Cancelada', 'Cancelada')],
        default='Pendiente'
    )

    def __str__(self):
        return f"Nota de Crédito {self.id} - {self.monto} - {self.estado}"
#########################################################################################


# MODELO PARA DEVOLUCIONES A PROVEEDORES
class DevolucionCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='devoluciones')
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Aprobada', 'Aprobada'), ('Rechazada', 'Rechazada')],
        default='Pendiente'
    )
    usuario = models.CharField(max_length=100, blank=True, null=True)  # Quién procesa la devolución

    def __str__(self):
        return f"Devolución {self.id} - Compra {self.compra.id} - {self.estado}"


# MODELO PARA DETALLES DE DEVOLUCIONES A PROVEEDORES
class DetalleDevolucionCompra(models.Model):
    devolucion = models.ForeignKey(DevolucionCompra, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    motivo_detalle = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.descripcion} - Devolución {self.devolucion.id}"


