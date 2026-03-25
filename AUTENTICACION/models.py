from django.conf import settings
from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('supervisor', 'Supervisor'),
        ('cliente', 'Cliente'),
        ('mesero', 'Mesero'),
        ('cocinero', 'Cocinero'),
        ('cajero', 'Cajero')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')

    def save(self, *args, **kwargs):
        # Staff y superusuarios siempre son admin
        if self.is_staff or self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == 'admin'
    @property
    def is_vendedor(self):
        return self.role == 'vendedor'
    @property
    def is_supervisor(self):
        return self.role == 'supervisor'
    @property
    def is_mesero_role(self):
        return self.role == 'mesero'
    @property
    def is_cocinero_role(self):
        return self.role == 'cocinero'
    @property
    def is_cajero_role(self):
        return self.role == 'cajero'
    

class PasswordResetCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='password_reset_codes'
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} – {self.code}"
    
class ConfiguracionServidor(models.Model):
    ## NEW
    clave = models.CharField(max_length=100, null=True, blank=True)
    valor = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    url_endpoint = models.CharField(max_length=200, blank=True, null=True)
    contraseña = models.CharField(max_length=255, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True)
    descripcion = models.CharField(max_length=300, null=True, blank=True)
    def __str__(self):
        return f"{self.clave}"
    
class UsuarioEmisor(models.Model):
    """
    Relación entre usuarios y emisores. Permite varios emisores por usuario,
    marcar uno como predeterminado, y activar/desactivar la relación.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emisores_rel")
    emisor = models.ForeignKey("FE.Emisor_fe", on_delete=models.CASCADE, related_name="usuarios_rel")
    activo = models.BooleanField(default=True)
    es_predeterminado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "emisor")
        verbose_name = "Vínculo Usuario–Emisor"
        verbose_name_plural = "Vínculos Usuario–Emisor"

    def __str__(self):
        return f"{self.user} → {self.emisor} ({'pred.' if self.es_predeterminado else 'sec.'})"
    
# Tu modelo Perfilusuario ya existe; solo añadimos el emisor activo:
class Perfilusuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # NUEVO: emisor activo
    emisor_activo = models.ForeignKey(
        "FE.Emisor_fe", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="usuarios_activos"
    )

    def __str__(self):
        return f"{self.user.email} – {self.nombre or ''} {self.apellido or ''}".strip()


class EmailProfile(models.Model):
    SCOPE_CHOICES = (
        ('general', 'General'),
        ('fe', 'Facturación Electrónica'),
    )
    nombre       = models.CharField(max_length=100, unique=True)
    scope        = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='general', db_index=True)
    host         = models.CharField(max_length=200)
    port         = models.PositiveIntegerField(default=465)
    use_ssl      = models.BooleanField(default=True)
    use_tls      = models.BooleanField(default=False)
    username     = models.CharField(max_length=200)
    password     = models.CharField(max_length=255)
    from_email   = models.EmailField(help_text="Remitente por defecto (FROM)")
    is_active    = models.BooleanField(default=True)
    notes        = models.TextField(blank=True, default="")
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil de correo"
        verbose_name_plural = "Perfiles de correo"

    def __str__(self):
        return f"{self.nombre} [{self.scope}]{' *' if self.is_active else ''}"

class Plan(models.Model):
    """Plan comercial que determina qué módulos tiene disponibles un emisor."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    tiene_facturacion  = models.BooleanField(default=True,  verbose_name="Facturación Electrónica")
    tiene_ventas       = models.BooleanField(default=True,  verbose_name="Ventas")
    tiene_compras      = models.BooleanField(default=False, verbose_name="Compras")
    tiene_inventario   = models.BooleanField(default=False, verbose_name="Inventario")
    tiene_contabilidad = models.BooleanField(default=False, verbose_name="Contabilidad")
    tiene_rrhh         = models.BooleanField(default=False, verbose_name="RRHH / Nómina")
    tiene_restaurante  = models.BooleanField(default=False, verbose_name="Restaurante / POS")

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"

    def __str__(self):
        return self.nombre


class Suscripcion(models.Model):
    """Vincula un Emisor a un Plan con fechas de vigencia."""
    emisor      = models.OneToOneField("FE.Emisor_fe", on_delete=models.CASCADE, related_name="suscripcion")
    plan        = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="suscripciones")
    fecha_inicio = models.DateField()
    fecha_fin    = models.DateField(null=True, blank=True, help_text="Dejar vacío = sin vencimiento")
    activo       = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"

    def esta_vigente(self):
        """Activa si no ha expirado O está dentro del periodo de gracia (24h)."""
        from datetime import timedelta
        from django.utils import timezone
        if not self.activo:
            return False
        if self.fecha_fin:
            hoy = timezone.now().date()
            limite_gracia = self.fecha_fin + timedelta(days=1)
            if hoy > limite_gracia:
                return False
        return True

    def en_periodo_gracia(self):
        """True si la fecha_fin ya pasó pero aún está dentro de las 24h de gracia."""
        from datetime import timedelta
        from django.utils import timezone
        if not self.activo or not self.fecha_fin:
            return False
        hoy = timezone.now().date()
        return self.fecha_fin < hoy <= self.fecha_fin + timedelta(days=1)

    @property
    def gracia_fin(self):
        """Fecha+hora exacta en que termina el periodo de gracia (medianoche del día siguiente)."""
        from datetime import timedelta, datetime, time
        from django.utils import timezone
        if self.fecha_fin:
            fin = datetime.combine(self.fecha_fin + timedelta(days=1), time.max)
            return timezone.make_aware(fin) if timezone.is_naive(fin) else fin
        return None

    def __str__(self):
        return f"{self.emisor} → {self.plan}"


# Crear automáticamente el perfil al crear el usuario
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfilusuario.objects.create(user=instance)