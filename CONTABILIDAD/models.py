from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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
