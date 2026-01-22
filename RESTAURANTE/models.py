from collections import defaultdict
from django.conf import settings
from django.db import models
from django.db.models import Q, Max
from django.contrib.auth.models import User
from decimal import ROUND_HALF_UP, Decimal
from django.utils import timezone
from AUTENTICACION.models import Perfilusuario
from INVENTARIO.models import Producto
from django.db import  transaction
from django.db.models import Sum 

#####################################################################################################
#                                 CONFIGURAICÓN RESTAURANTE                                         #
#####################################################################################################

class Area(models.Model):
    """Areas del restaurante donde se encuntran las mesas"""
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del area")

    class Meta:
        verbose_name = "Area restaurante"
        verbose_name_plural = "Areas restaurante"
        
    def __str__(self):
        return f"Area restaurante: {self.nombre}"
    
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
    
class Mesa(models.Model):
    """Representa las mesas físicas o áreas de servicio del restaurante."""
    ESTADO_MESA_CHOICES = [
        ('LIBRE', 'Libre'),
        ('OCUPADA', 'Ocupada'),
        ("ENTREGADO", "Entregado"),
        ('PENDIENTE_ORDEN', 'Pendiente de Orden'),
        ('PENDIENTE_PAGO', 'Pendiente de Pago'),
        ('PAGADO', 'Pagado'),
    ]
    
    numero = models.CharField(max_length=10, unique=True, verbose_name="Número de Mesa")
    capacidad = models.PositiveSmallIntegerField(default=4, verbose_name="Capacidad de personas")
    area = models.ForeignKey("RESTAURANTE.Area",on_delete=models.SET_NULL,null=True, blank=True,related_name="area",
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
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="platillo",
    )
    
    area_cocina = models.ForeignKey("RESTAURANTE.AreaCocina", verbose_name=("area cocina"), on_delete=models.SET_NULL, null=True, blank=True)
    
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

#####################################################################################################
#                                            MESEROS                                               #
#####################################################################################################

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


class AsignacionMesa(models.Model):
    """Registro de los meseros que estan acargo de atender las mesas"""
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name="asignaciones")
    mesero = models.ForeignKey(Mesero, on_delete=models.CASCADE, related_name="asignaciones")
    es_fija = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(default=timezone.now, verbose_name="fecha inicio")
    fecha_fin = models.DateTimeField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Asignacion de mesa"
        verbose_name_plural = "Asignaciones de mesas"

        
    def __str__(self):
        return f"{self.mesa} - {self.mesero} - {self.fecha_inicio} - {self.fecha_fin}"
#####################################################################################################
#                                              COCINA                                               #
#####################################################################################################

class AreaCocina(models.Model):
    """Areas de cocina donde pertenecen los platillos para enviarlo a comanda"""
    area_cocina = models.CharField(max_length=50, unique=True, verbose_name="Nombre del area de cocina")

    class Meta:
        verbose_name = "Area de codina"
        verbose_name_plural = "Areas de cocina"
        
    def __str__(self):
        return f"Area cocina: {self.area_cocina}"
    
class Cocinero(models.Model):
    """Perfil que liga un usuario del sistema al rol de mesero."""
    nombre = models.CharField(max_length=120, null=False, verbose_name="Nombre cocinero")
    pin = models.CharField(max_length=20, unique=True, verbose_name="codigo de identificaciòn") 
    activo = models.BooleanField(default=True, verbose_name="Cocinero activo")
    area_cocina = models.ForeignKey("RESTAURANTE.AreaCocina",on_delete=models.SET_NULL,null=True, blank=True )
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Cocinero"
        verbose_name_plural = "Cocineros"
    
    def __str__(self):
        return self.pin 
    

    
class Pedido(models.Model):
    """Orden de comida de las mesas"""
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
    division_confirmada = models.BooleanField(default=False)
    
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
    def marcar_pagado_si_corresponde(self):
        """
        Marca el pedido como PAGADO si todas las cuentas del pedido
        están en estado PAGADA o ANULADA.
        """
        # Releer con lock para evitar race conditions
        pedido = Pedido.objects.select_for_update().get(id=self.id)

        print(">>>> PEDIDO PAGADO MODEL ", pedido)
        # Si ya está pagado, no hagas nada
        if pedido.estado == "PAGADO":
            return False

        # Considera como "resueltas" las cuentas PAGADAS o ANULADAS
        pendientes = pedido.cuentas.exclude(estado__in=["PAGADA", "ANULADA"]).exists()
        if pendientes:
            return False

        pedido.estado = "PAGADO"
        pedido.pagado_el = timezone.now()
        pedido.save(update_fields=["estado", "pagado_el"])
        print(">>>> PEDIDO PAGADO MODEL ", pedido.estado)

        # tu mesa: si quieres LIBRE, usa LIBRE. Si tienes PAGADO, úsalo.
        pedido.mesa.estado = "PAGADO"  # o "PAGADO" si así lo manejas
        pedido.mesa.save(update_fields=["estado"])

        return True
    
    @transaction.atomic
    def crear_comandas_por_area(self):
        """
        Crea una comanda por cada área de cocina involucrada
        y agrega solo los platillos correspondientes.
        """

        detalles = (
            self.detalles
            .select_related("platillo", "platillo__area_cocina")
            .filter(platillo__es_preparado=True)
        )

        detalles_por_area = defaultdict(list)

        for d in detalles:
            if d.platillo.area_cocina:
                detalles_por_area[d.platillo.area_cocina].append(d)

        comandas_creadas = []

        for area, detalles_area in detalles_por_area.items():
            # ¿Ya hay comanda activa para esa área?
            comanda = (
                self.comandas
                .filter(
                    area_cocina=area,
                    estado__in=["ENVIADA", "EN_PREPARACION"]
                )
                .first()
            )

            if not comanda:
                last_num = (
                    self.comandas
                    .select_for_update()
                    .aggregate(m=Max("numero"))
                    .get("m") or 0
                )

                comanda = Comanda.objects.create(
                    pedido=self,
                    area_cocina=area,
                    numero=last_num + 1
                )

            for detalle in detalles_area:
                # Evita duplicados
                if not comanda.items.filter(detalle_pedido=detalle).exists():
                    ComandaItem.from_detalle(
                        comanda=comanda,
                        detalle=detalle
                    )

            comandas_creadas.append(comanda)

        return comandas_creadas


class DetallePedido(models.Model):
    """Detalle de cada plato ingresado al pedido"""
        
    pedido = models.ForeignKey("RESTAURANTE.Pedido", on_delete=models.CASCADE, related_name="detalles")
    platillo = models.ForeignKey("RESTAURANTE.Platillo", on_delete=models.PROTECT, related_name="detalles_pedido")

    cuenta = models.ForeignKey(
        "RESTAURANTE.CuentaPedido",
        on_delete=models.PROTECT,
        related_name="detalles",
        null=True,
        blank=True,
    )

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
        indexes = [
            models.Index(fields=["pedido", "cuenta"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(cantidad__gte=0),
                name="detallepedido_cantidad_gte_0",
            ),
        ]

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


class Comanda(models.Model):
    """Lista de platillos a preparar en cocina"""
    ESTADO_COMANDA = [
        ("ENVIADA", "Enviada"),
        ("EN_PREPARACION", "En preparación"),
        ("CERRADA", "Cerrada"),
        ("ANULADA", "Anulada"),
    ]

    pedido = models.ForeignKey("RESTAURANTE.Pedido", on_delete=models.CASCADE, related_name="comandas")
    numero = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADO_COMANDA, default="ENVIADA")

    area_cocina = models.ForeignKey(
        "RESTAURANTE.AreaCocina",
        on_delete=models.PROTECT,
        related_name="comandas"
    )

    creada_el = models.DateTimeField(default=timezone.now)
    iniciada_el = models.DateTimeField(null=True, blank=True)
    cerrada_el = models.DateTimeField(null=True, blank=True)

    notas = models.CharField(max_length=250, blank=True, default="")

    class Meta:
        ordering = ["-creada_el"]
        constraints = [
            models.UniqueConstraint(
                fields=["pedido", "numero"], 
                name="uniq_comanda_por_pedido_numero"
            ),
            models.UniqueConstraint(
                fields=["pedido", "area_cocina", "estado"],
                condition=Q(estado__in=["ENVIADA", "EN_PREPARACION"]),
                name="uniq_comanda_activa_por_area"
            )
        ]

    @classmethod
    @transaction.atomic
    def crear_para_pedido(cls, pedido, *, notas=""):
        last_num = (
            cls.objects
            .select_for_update()
            .filter(pedido=pedido)
            .aggregate(m=Max("numero"))
            .get("m") or 0
        )
        return cls.objects.create(
            pedido=pedido,
            numero=last_num + 1,
            notas=notas
        )

class ComandaItem(models.Model):
    comanda = models.ForeignKey("RESTAURANTE.Comanda", on_delete=models.CASCADE, related_name="items")
    detalle_pedido = models.ForeignKey("RESTAURANTE.DetallePedido", on_delete=models.PROTECT, related_name="comanda_items")

    # snapshot
    nombre = models.CharField(max_length=160)
    cantidad = models.PositiveIntegerField(default=1)
    notas = models.CharField(max_length=250, blank=True, default="")


    enviado_el = models.DateTimeField(default=timezone.now)
    iniciado_el = models.DateTimeField(null=True, blank=True)
    listo_el = models.DateTimeField(null=True, blank=True)
    entregado_el = models.DateTimeField(null=True, blank=True)


    class Meta:
        ordering = ["id"]

    @classmethod
    def from_detalle(cls, comanda, detalle, *, notas=""):
        return cls.objects.create(
            comanda=comanda,
            detalle_pedido=detalle,
            nombre=detalle.platillo.nombre,
            cantidad=detalle.cantidad,
            notas=(notas or detalle.notas or ""),
        )

#####################################################################################################
#                                          CAJA Y CUENTA                                            #
#####################################################################################################

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
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Caja #{self.id} - {self.estado}"
    
    # def calcular_totales(self):
        
    #     detalles = self.detalles_arqueo.filter(tipo='CIERRE').select_related("denominacion")
    #     total_fisico = sum((d.denominacion.valor * d.cantidad) for d in detalles)
    #     self.monto_final = total_fisico.quantize(Decimal("0.01"))
    #     esperado = (self.monto_inicial + self.total_efectivo).quantize(Decimal("0.01"))
    #     self.diferencia = (self.monto_final - esperado).quantize(Decimal("0.01"))
    #     print("CALCULAR TOTALES DENTRO DE MODAL ", (self.monto_final))
    #     self.save(update_fields=["monto_final", "diferencia"])

# Movimientos que no vienen de ventas (fondos adicionales, agregar sencillo, pago a proveedrores, compras o adelanto)
class MovimientosCaja(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('RETIRO', 'Retiro'),
    ]
    tipo_movimiento = models.CharField(
        max_length=20,
        choices=TIPO_MOVIMIENTO_CHOICES
    )
    CATEGORIA_CHOICES = [
        ('PROVEEDOR', 'Pago a Proveedor'),
        ('COMPRA_LOCAL', 'Compra Insumos'),
        ('NOMINA', 'Adelanto Sueldo'),
        ('OTROS', 'Otros'),
    ]
    
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='OTROS')
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name="movimientos")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=200)
    fecha = models.DateTimeField(default=timezone.now)
    autorizado_por = models.ForeignKey(Perfilusuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto}"

#Tipo_billetes_monedas (pos_bill)
class BilletesYMonedas(models.Model):    
    # Denominación: 20.00, 10.00, 5.00, 1.00, 0.25, 0.10, 0.05, 0.01
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre} - ${self.valor}"
    
# Cantidad de billetes y monedas
class CajaDetalleArqueo(models.Model):
    TIPO = [
        ("APERTURA", "Apertura"),
        ("CIERRE", "Cierre"),
    ]

    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name="detalles_arqueo")
    denominacion = models.ForeignKey(BilletesYMonedas, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10, choices=TIPO)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["caja", "denominacion", "tipo"],
                name="uniq_caja_denominacion_tipo"
            )
        ]

    @property
    def subtotal(self):
        return (self.denominacion.valor or Decimal("0.00")) * Decimal(self.cantidad)


class CuentaPedido(models.Model):
    ESTADO = [
        ("ABIERTA", "Abierta"),
        ("CERRADA", "Cerrada"),
        ("PAGADA", "Pagada"),
        ("ANULADA", "Anulada"),
    ]
    factura = models.OneToOneField("FE.FacturaElectronica", on_delete=models.SET_NULL, null=True, blank=True, related_name="cuenta_pedido",)
    pedido = models.ForeignKey("RESTAURANTE.Pedido", on_delete=models.CASCADE, related_name="cuentas")
    nombre = models.CharField(max_length=60, default="Cuenta")
    estado = models.CharField(max_length=20, choices=ESTADO, default="ABIERTA")

    creado_el = models.DateTimeField(default=timezone.now)
    cerrado_el = models.DateTimeField(null=True, blank=True)
    pagado_el = models.DateTimeField(null=True, blank=True)

    # totales por cuenta (igual que Pedido)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    descuento_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    iva_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    propina = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        indexes = [models.Index(fields=["pedido", "estado"])]
        
    def recalcular_totales(self, save=True):
        print("RECALCULAR")
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
    
class Cajero(models.Model):
    """Perfil que liga un usuario del sistema al rol de cajero"""
    nombre = models.CharField(max_length=120, null=False, verbose_name="Nombre Cajero")
    pin = models.CharField(max_length=20, unique=True, verbose_name="codigo de identificaciòn") 
    activo = models.BooleanField(default=True, verbose_name="Cajero activo")
    area_cocina = models.ForeignKey("RESTAURANTE.AreaCocina",on_delete=models.SET_NULL,null=True, blank=True )
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Cajero"
        verbose_name_plural = "Cajeros"
    
    def __str__(self):
        return self.pin 