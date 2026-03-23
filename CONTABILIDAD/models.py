from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date

User = get_user_model()


class CuentaContable(models.Model):
    TIPO_CHOICES = [
        ('ACTIVO',   'Activo'),
        ('PASIVO',   'Pasivo'),
        ('CAPITAL',  'Capital'),
        ('INGRESO',  'Ingreso'),
        ('GASTO',    'Gasto'),
    ]
    NATURALEZA_CHOICES = [
        ('DEUDORA',   'Deudora'),
        ('ACREEDORA', 'Acreedora'),
    ]
    NIVEL_CHOICES = [
        ('PADRE',   'Padre (agrupadora)'),
        ('DETALLE', 'Detalle (recibe movimientos)'),
    ]

    codigo       = models.CharField(max_length=20, unique=True)
    nombre       = models.CharField(max_length=200)
    tipo         = models.CharField(max_length=10, choices=TIPO_CHOICES)
    naturaleza   = models.CharField(max_length=10, choices=NATURALEZA_CHOICES)
    nivel        = models.CharField(max_length=10, choices=NIVEL_CHOICES, default='DETALLE')
    cuenta_padre = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='subcuentas'
    )
    descripcion  = models.TextField(blank=True)
    activa       = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Cuenta Contable'
        verbose_name_plural = 'Cuentas Contables'
        ordering            = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'

    @property
    def saldo(self):
        """Saldo calculado a partir de todas las líneas de asiento confirmadas."""
        from django.db.models import Sum
        lineas = self.lineas.filter(asiento__estado='CONFIRMADO')
        debe  = lineas.aggregate(t=Sum('debe'))['t']  or 0
        haber = lineas.aggregate(t=Sum('haber'))['t'] or 0
        if self.naturaleza == 'DEUDORA':
            return debe - haber
        return haber - debe


class AsientoContable(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR',   'Borrador'),
        ('CONFIRMADO', 'Confirmado'),
    ]

    numero     = models.PositiveIntegerField(unique=True, editable=False)
    fecha      = models.DateField()
    concepto   = models.CharField(max_length=500)
    periodo    = models.CharField(max_length=7, help_text='Formato YYYY-MM', blank=True)
    estado     = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='BORRADOR')
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Asiento Contable'
        verbose_name_plural = 'Asientos Contables'
        ordering            = ['-fecha', '-numero']

    def __str__(self):
        return f'Asiento #{self.numero} – {self.fecha}'

    def save(self, *args, **kwargs):
        if not self.pk:
            ultimo = AsientoContable.objects.order_by('-numero').first()
            self.numero = (ultimo.numero + 1) if ultimo else 1
        if not self.periodo and self.fecha:
            self.periodo = self.fecha.strftime('%Y-%m')
        super().save(*args, **kwargs)

    @property
    def total_debe(self):
        from django.db.models import Sum
        return self.lineas.aggregate(t=Sum('debe'))['t'] or 0

    @property
    def total_haber(self):
        from django.db.models import Sum
        return self.lineas.aggregate(t=Sum('haber'))['t'] or 0

    @property
    def esta_cuadrado(self):
        return self.total_debe == self.total_haber


class LineaAsiento(models.Model):
    asiento     = models.ForeignKey(AsientoContable, on_delete=models.CASCADE, related_name='lineas')
    cuenta      = models.ForeignKey(CuentaContable, on_delete=models.PROTECT, related_name='lineas')
    descripcion = models.CharField(max_length=300, blank=True)
    debe        = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    haber       = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        verbose_name        = 'Línea de Asiento'
        verbose_name_plural = 'Líneas de Asiento'

    def __str__(self):
        return f'{self.cuenta} | D:{self.debe} H:{self.haber}'

    def clean(self):
        if self.debe < 0 or self.haber < 0:
            raise ValidationError('Los valores de debe y haber no pueden ser negativos.')
        if self.debe > 0 and self.haber > 0:
            raise ValidationError('Una línea no puede tener debe y haber al mismo tiempo.')
        if self.debe == 0 and self.haber == 0:
            raise ValidationError('La línea debe tener un valor en debe o haber.')
        if self.cuenta.nivel != 'DETALLE':
            raise ValidationError('Solo se pueden usar cuentas de detalle en los asientos.')


# ─────────────────────────────────────────────────────────────────────────────
# CUENTAS POR COBRAR
# ─────────────────────────────────────────────────────────────────────────────

class CuentaPorCobrar(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL',   'Parcial'),
        ('PAGADO',    'Pagado'),
        ('VENCIDO',   'Vencido'),
        ('ANULADO',   'Anulado'),
    ]

    factura          = models.ForeignKey(
        'FE.FacturaElectronica', on_delete=models.PROTECT,
        related_name='cuentas_cobrar'
    )
    receptor         = models.ForeignKey(
        'FE.Receptor_fe', on_delete=models.PROTECT,
        related_name='cuentas_cobrar'
    )
    fecha_emision    = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_original   = models.DecimalField(max_digits=14, decimal_places=2)
    estado           = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    notas            = models.TextField(blank=True)
    creado_por       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Cuenta por Cobrar'
        verbose_name_plural = 'Cuentas por Cobrar'
        ordering            = ['fecha_vencimiento']

    def __str__(self):
        return f'CxC #{self.pk} – {self.receptor.nombre} ${self.monto_original}'

    @property
    def monto_pagado(self):
        return self.pagos.aggregate(t=Sum('monto'))['t'] or 0

    @property
    def saldo_pendiente(self):
        return self.monto_original - self.monto_pagado

    @property
    def esta_vencida(self):
        return self.fecha_vencimiento < date.today() and self.estado in ('PENDIENTE', 'PARCIAL')

    def actualizar_estado(self):
        if self.estado == 'ANULADO':
            return
        if self.saldo_pendiente <= 0:
            self.estado = 'PAGADO'
        elif self.monto_pagado > 0:
            self.estado = 'PARCIAL'
        elif self.esta_vencida:
            self.estado = 'VENCIDO'
        self.save(update_fields=['estado'])


class PagoCobro(models.Model):
    FORMA_PAGO_CHOICES = [
        ('EFECTIVO',      'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia bancaria'),
        ('CHEQUE',        'Cheque'),
        ('TARJETA',       'Tarjeta'),
        ('OTRO',          'Otro'),
    ]

    cuenta_cobrar    = models.ForeignKey(CuentaPorCobrar, on_delete=models.CASCADE, related_name='pagos')
    fecha            = models.DateField()
    monto            = models.DecimalField(max_digits=14, decimal_places=2)
    forma_pago       = models.CharField(max_length=15, choices=FORMA_PAGO_CHOICES)
    referencia       = models.CharField(max_length=100, blank=True)
    notas            = models.TextField(blank=True)
    # Cuenta débito (ej. Caja o Banco) y cuenta crédito (CxC) para el asiento
    cuenta_debito    = models.ForeignKey(
        CuentaContable, on_delete=models.PROTECT,
        related_name='pagos_cobro_debito', null=True, blank=True
    )
    cuenta_credito   = models.ForeignKey(
        CuentaContable, on_delete=models.PROTECT,
        related_name='pagos_cobro_credito', null=True, blank=True
    )
    asiento          = models.ForeignKey(
        AsientoContable, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='pagos_cobro'
    )
    creado_por       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Pago de Cobro'
        verbose_name_plural = 'Pagos de Cobro'
        ordering            = ['-fecha']

    def __str__(self):
        return f'Pago ${self.monto} – {self.fecha}'

    def generar_asiento(self):
        """Genera y confirma el asiento contable de este pago."""
        if not self.cuenta_debito or not self.cuenta_credito:
            return None
        asiento = AsientoContable.objects.create(
            fecha=self.fecha,
            concepto=f'Cobro CxC #{self.cuenta_cobrar_id} – {self.cuenta_cobrar.receptor.nombre}',
            estado='CONFIRMADO',
            creado_por=self.creado_por,
        )
        LineaAsiento.objects.create(asiento=asiento, cuenta=self.cuenta_debito,  debe=self.monto, haber=0)
        LineaAsiento.objects.create(asiento=asiento, cuenta=self.cuenta_credito, debe=0, haber=self.monto)
        self.asiento = asiento
        self.save(update_fields=['asiento'])
        return asiento


# ─────────────────────────────────────────────────────────────────────────────
# CUENTAS POR PAGAR
# ─────────────────────────────────────────────────────────────────────────────

class CuentaPorPagar(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL',   'Parcial'),
        ('PAGADO',    'Pagado'),
        ('VENCIDO',   'Vencido'),
        ('ANULADO',   'Anulado'),
    ]

    compra           = models.ForeignKey(
        'INVENTARIO.Compra', on_delete=models.PROTECT,
        related_name='cuentas_pagar'
    )
    proveedor        = models.ForeignKey(
        'INVENTARIO.Proveedor', on_delete=models.PROTECT,
        related_name='cuentas_pagar'
    )
    fecha_emision    = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_original   = models.DecimalField(max_digits=14, decimal_places=2)
    estado           = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    notas            = models.TextField(blank=True)
    creado_por       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Cuenta por Pagar'
        verbose_name_plural = 'Cuentas por Pagar'
        ordering            = ['fecha_vencimiento']

    def __str__(self):
        return f'CxP #{self.pk} – {self.proveedor.nombre} ${self.monto_original}'

    @property
    def monto_pagado(self):
        return self.pagos.aggregate(t=Sum('monto'))['t'] or 0

    @property
    def saldo_pendiente(self):
        return self.monto_original - self.monto_pagado

    @property
    def esta_vencida(self):
        return self.fecha_vencimiento < date.today() and self.estado in ('PENDIENTE', 'PARCIAL')

    def actualizar_estado(self):
        if self.estado == 'ANULADO':
            return
        if self.saldo_pendiente <= 0:
            self.estado = 'PAGADO'
        elif self.monto_pagado > 0:
            self.estado = 'PARCIAL'
        elif self.esta_vencida:
            self.estado = 'VENCIDO'
        self.save(update_fields=['estado'])


class PagoPagar(models.Model):
    FORMA_PAGO_CHOICES = [
        ('EFECTIVO',      'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia bancaria'),
        ('CHEQUE',        'Cheque'),
        ('TARJETA',       'Tarjeta'),
        ('OTRO',          'Otro'),
    ]

    cuenta_pagar     = models.ForeignKey(CuentaPorPagar, on_delete=models.CASCADE, related_name='pagos')
    fecha            = models.DateField()
    monto            = models.DecimalField(max_digits=14, decimal_places=2)
    forma_pago       = models.CharField(max_length=15, choices=FORMA_PAGO_CHOICES)
    referencia       = models.CharField(max_length=100, blank=True)
    notas            = models.TextField(blank=True)
    # Cuenta débito (CxP) y cuenta crédito (ej. Caja o Banco) para el asiento
    cuenta_debito    = models.ForeignKey(
        CuentaContable, on_delete=models.PROTECT,
        related_name='pagos_pagar_debito', null=True, blank=True
    )
    cuenta_credito   = models.ForeignKey(
        CuentaContable, on_delete=models.PROTECT,
        related_name='pagos_pagar_credito', null=True, blank=True
    )
    asiento          = models.ForeignKey(
        AsientoContable, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='pagos_pagar'
    )
    creado_por       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Pago a Proveedor'
        verbose_name_plural = 'Pagos a Proveedores'
        ordering            = ['-fecha']

    def __str__(self):
        return f'Pago ${self.monto} – {self.fecha}'

    def generar_asiento(self):
        """Genera y confirma el asiento contable de este pago."""
        if not self.cuenta_debito or not self.cuenta_credito:
            return None
        asiento = AsientoContable.objects.create(
            fecha=self.fecha,
            concepto=f'Pago CxP #{self.cuenta_pagar_id} – {self.cuenta_pagar.proveedor.nombre}',
            estado='CONFIRMADO',
            creado_por=self.creado_por,
        )
        LineaAsiento.objects.create(asiento=asiento, cuenta=self.cuenta_debito,  debe=self.monto, haber=0)
        LineaAsiento.objects.create(asiento=asiento, cuenta=self.cuenta_credito, debe=0, haber=self.monto)
        self.asiento = asiento
        self.save(update_fields=['asiento'])
        return asiento
