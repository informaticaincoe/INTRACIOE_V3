from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from decimal import ROUND_HALF_UP, Decimal
from django.utils import timezone
from AUTENTICACION.models import Perfilusuario
from INVENTARIO.models import Producto
from django.db import  transaction
from django.db.models import Sum 

class CategoriaMenu(models.Model):
    """Define la categoría a la que pertenece un platillo o bebida (e.g., Entrada, Plato Fuerte)."""
    
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    color = models.CharField(
            max_length=7, 
            default='#007bff', # Color por defecto (ej: azul de Bootstrap)
            verbose_name="Color (Hexadecimal)"
        )
    class Meta:
        verbose_name = "Categoría del Menú"
        verbose_name_plural = "Categorías del Menú"

    def __str__(self):
        return self.nombre

class Mesero(models.Model):
    """Perfil que liga un usuario del sistema al rol de mesero."""
    # Se usa OneToOneField para asegurar que cada usuario sea un Mesero único.
    nombre = models.CharField(max_length=120, null=False, verbose_name="Nombre mesero")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="codigo de identificaciòn") 
    activo = models.BooleanField(default=True, verbose_name="Mesero Activo")
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Mesero"
        verbose_name_plural = "Meseros"
    
    def __str__(self):
        return self.codigo 

class Area(models.Model):
    """Areas del restaurante donde se encuntran las mesas"""
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Número de Mesa")

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"
        
    def __str__(self):
        return f"Area: {self.nombre}"
    
class Mesa(models.Model):
    """Representa las mesas físicas o áreas de servicio del restaurante."""
    ESTADO_MESA_CHOICES = [
        ('LIBRE', 'Libre'),
        ('OCUPADA', 'Ocupada'),
        ('PENDIENTE_ORDEN', 'Pendiente de Orden'),
        ('PENDIENTE_PAGO', 'Pendiente de Pago'),
    ]
    numero = models.CharField(max_length=10, unique=True, verbose_name="Número de Mesa")
    capacidad = models.PositiveSmallIntegerField(default=4, verbose_name="Capacidad de personas")
    area = models.ForeignKey("RESTAURANTE.Area",on_delete=models.SET_NULL,null=True, blank=True,related_name="mesas",
    )
    es_vip = models.BooleanField(default=False, verbose_name="Mesa VIP (Prioridad)")
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_MESA_CHOICES,
        default='LIBRE',
        verbose_name="Estado Actual"
    )
    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        
    def __str__(self):
        return f"Mesa {self.numero} ({self.area})"

class AsignacionMesa(models.Model):
    
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name="asignaciones")
    mesero = models.ForeignKey(Mesero, on_delete=models.CASCADE, related_name="asignaciones")
    es_fija = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(default=timezone.now, verbose_name="fecha inicio")
    fecha_fin = models.DateTimeField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Asignacion de mesa"
        verbose_name_plural = "Asignaciones de mesas"
        
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["mesa"],
        #         condition=Q(activa=True),
        #         name="uniq_mesa_asignacion_activa"
        #     )
        # ]
        
    def __str__(self):
        return f"{self.mesa} - {self.mesero} - {self.fecha_inicio} - {self.fecha_fin}"

class Platillo(models.Model):
    """Representa los ítems vendibles del menú."""
    codigo = models.CharField(max_length=50, unique=True) 
    categoria = models.ForeignKey(CategoriaMenu, on_delete=models.PROTECT, related_name='platillos')
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Platillo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción o Ingredientes")
    imagen = models.ImageField(upload_to='Menu/', null=True, blank=True)
    precio_venta = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        verbose_name="Precio de Venta"
    )
    disponible = models.BooleanField(default=True, verbose_name="Disponible para Venta")
    # Indicador para Cocina (si requiere preparación activa vs. es un producto embotellado)
    es_preparado = models.BooleanField(default=True, verbose_name="Requiere Cocina/Preparación")
    
    producto = models.OneToOneField(
        "INVENTARIO.Producto",
        on_delete=models.PROTECT,   # mejor que CASCADE (para no borrar producto por error)
        null=True,
        blank=True,
        related_name="platillo",
    )
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        creando = self.pk is None
        super().save(*args, **kwargs)  # primero guarda para tener pk

        # Si no tiene producto, créalo
        if self.producto_id is None:
            prod = Producto.objects.create(
                codigo=self.codigo,
                descripcion=self.nombre,
                precio_venta=self.precio_venta,
                preunitario=self.precio_venta,  # si aplica en tu lógica
                
                precio_compra=0,
                stock=0 if self.es_preparado else 0,  # puedes dejar 0 y manejar compras
                stock_minimo=0,
                stock_maximo=0,
                # setea defaults requeridos en tu modelo:
                tributo_id=1,
                precio_iva=False,
                imagen=self.imagen
            )
            self.producto = prod
            super().save(update_fields=["producto"])

        else:
            # Si ya existe, sincroniza campos clave (opcional)
            Producto.objects.filter(pk=self.producto_id).update(
                descripcion=self.nombre,
                precio_venta=self.precio_venta,
            )

    class Meta:
        verbose_name = "Platillo / Ítem del Menú"
        verbose_name_plural = "Platillos / Ítems del Menú"

    def __str__(self):
        return self.nombre
    
###############################################################################################
# CAJA
###############################################################################################

class Caja(models.Model):
    ESTADO_CAJA_CHOICES = [
        ('ABIERTA', 'Abierta'),
        ('CERRADA', 'Cerrada'),
    ]

    usuario = models.ForeignKey(Perfilusuario, on_delete=models.CASCADE)
    fecha_apertura = models.DateTimeField(default=timezone.now, verbose_name="Fecha de apertura")
    fecha_cierre = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de cierre")

    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    monto_cierre = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    total_ventas = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_tarjeta = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    monto_final = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    total_propinas = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CAJA_CHOICES,
        default='ABIERTA'
    )

    def __str__(self):
        return f"Caja #{self.id} - {self.estado}"

class MovimientosCaja(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('RETIRO', 'Retiro'),
    ]

    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name="movimientos")
    tipo_movimiento = models.CharField(
        max_length=20,
        choices=TIPO_MOVIMIENTO_CHOICES
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=200)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto}"

class Pedido(models.Model):
    ESTADO_PEDIDO = [
        ("ABIERTO", "Abierto"),           # hay orden en curso (mesa OCUPADA)
        ("CERRADO", "Cerrado"),           # ya pidieron cuenta (mesa PENDIENTE_PAGO)
        ("PAGADO", "Pagado"),             # ya se cobró (mesa LIBRE)
        ("ANULADO", "Anulado"),
    ]

    mesa = models.ForeignKey("RESTAURANTE.Mesa", on_delete=models.PROTECT, related_name="pedidos")
    mesero = models.ForeignKey("RESTAURANTE.Mesero", on_delete=models.PROTECT, related_name="pedidos")
    receptor = models.ForeignKey("FE.Receptor_fe", on_delete=models.SET_NULL, null=True, blank=True)

    # Se asigna cuando se paga
    caja = models.ForeignKey("RESTAURANTE.Caja", on_delete=models.PROTECT, null=True, blank=True, related_name="pedidos")
    factura = models.OneToOneField("FE.FacturaElectronica", on_delete=models.SET_NULL, null=True, blank=True, related_name="pedido_origen")

    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default="ABIERTO")
    creado_el = models.DateTimeField(default=timezone.now)
    cerrado_el = models.DateTimeField(null=True, blank=True)
    pagado_el = models.DateTimeField(null=True, blank=True)

    notas = models.CharField(max_length=300, blank=True, default="")

    # Totales “persistidos” (te sirve para reportes y caja)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    descuento_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    iva_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    propina = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["-creado_el"]
        indexes = [
            models.Index(fields=["mesa", "estado"]),
            models.Index(fields=["creado_el"]),
        ]

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa.numero} - {self.estado}"

    # ---------- Helpers de estado de mesa ----------
    def _sync_estado_mesa(self):
        """Alinea el estado de la Mesa según estado del pedido."""
        if self.estado == "ABIERTO":
            # si ya hay pedido, la mesa debería estar OCUPADA
            if self.mesa.estado != "OCUPADA":
                self.mesa.estado = "OCUPADA"
                self.mesa.save(update_fields=["estado"])
        elif self.estado == "CERRADO":
            if self.mesa.estado != "PENDIENTE_PAGO":
                self.mesa.estado = "PENDIENTE_PAGO"
                self.mesa.save(update_fields=["estado"])
        elif self.estado in ("PAGADO", "ANULADO"):
            if self.mesa.estado != "LIBRE":
                self.mesa.estado = "LIBRE"
                self.mesa.save(update_fields=["estado"])

    # ---------- Totales ----------
    def recalcular_totales(self, save=True):
        """
        Recalcula subtotal/descuento/iva/total desde DetallePedido.
        """
        agg = self.detalles.aggregate(
            sub=Sum("subtotal_linea"),
            desc=Sum("descuento_monto"),
            iva=Sum("iva_monto"),
            tot=Sum("total_linea"),
        )
        self.subtotal = (agg["sub"] or Decimal("0.00")).quantize(Decimal("0.01"))
        self.descuento_total = (agg["desc"] or Decimal("0.00")).quantize(Decimal("0.01"))
        self.iva_total = (agg["iva"] or Decimal("0.00")).quantize(Decimal("0.01"))

        base_total = (agg["tot"] or Decimal("0.00"))
        self.total = (base_total + (self.propina or Decimal("0.00"))).quantize(Decimal("0.01"))

        if save:
            self.save(update_fields=["subtotal", "descuento_total", "iva_total", "total"])

        return self.total

    # ---------- Flujo ----------
    @transaction.atomic
    def cerrar(self):
        if self.estado != "ABIERTO":
            return
        self.estado = "CERRADO"
        self.cerrado_el = timezone.now()
        self.recalcular_totales(save=True)
        self.save(update_fields=["estado", "cerrado_el"])
        self._sync_estado_mesa()

    @transaction.atomic
    def pagar_y_generar_factura_cf(self, *, usuario, caja, formas_pago_json=None, receptor=None):
        """
        1) valida estado
        2) recalcula totales
        3) crea FacturaElectronica (DTE 01) + DetalleFactura
        4) vincula pedido.factura
        5) marca PAGADO y libera mesa
        6) aquí también puedes registrar movimientos de caja
        """
        if self.estado != "CERRADO":
            raise ValueError("El pedido debe estar CERRADO (pendiente de pago) para poder pagarse.")

        if receptor:
            self.receptor = receptor

        self.caja = caja
        self.recalcular_totales(save=True)

        # --- Crear Factura CF desde el pedido ---
        # Import interno para evitar ciclos entre apps
        from FE.services import crear_factura_cf_desde_pedido  # lo definimos abajo

        factura = crear_factura_cf_desde_pedido(
            pedido=self,
            usuario=usuario,
            receptor=self.receptor,
            formas_pago_json=(formas_pago_json or []),
        )

        self.factura = factura
        self.estado = "PAGADO"
        self.pagado_el = timezone.now()
        self.save(update_fields=["factura", "estado", "pagado_el", "caja", "receptor"])

        # Mesa libre
        self._sync_estado_mesa()

        return factura


class DetallePedido(models.Model):
    pedido = models.ForeignKey("RESTAURANTE.Pedido", on_delete=models.CASCADE, related_name="detalles")
    platillo = models.ForeignKey("RESTAURANTE.Platillo", on_delete=models.PROTECT, related_name="detalles_pedido")

    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    # descuentos simples
    descuento_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))  # 0-100
    aplica_iva = models.BooleanField(default=True)

    # totales por línea “guardados”
    subtotal_linea = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    descuento_monto = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    iva_monto = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_linea = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    notas = models.CharField(max_length=250, blank=True, default="")
    creado_el = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.pedido_id} - {self.platillo.nombre} x {self.cantidad}"

    def _calc(self):
        # precio por defecto del platillo si no lo mandan
        if not self.precio_unitario or self.precio_unitario == Decimal("0.00"):
            self.precio_unitario = (self.platillo.precio_venta or Decimal("0.00"))

        qty = Decimal(str(self.cantidad))
        base = (qty * self.precio_unitario)

        desc_pct = (self.descuento_pct or Decimal("0.00"))
        desc_monto = (base * (desc_pct / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        neto = (base - desc_monto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        iva = Decimal("0.00")
        if self.aplica_iva:
            iva = (neto * Decimal("0.13")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        total = (neto + iva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        self.subtotal_linea = base.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.descuento_monto = desc_monto
        self.iva_monto = iva
        self.total_linea = total

    def save(self, *args, **kwargs):
        self._calc()
        super().save(*args, **kwargs)
        # cada vez que cambia una línea, recalcula totales del pedido
        self.pedido.recalcular_totales(save=True)
