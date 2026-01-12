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
        
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')

    def is_admin(self):
        return self.role == 'admin'

    def is_vendedor(self):
        return self.role == 'vendedor'

    def is_supervisor(self):
        return self.role == 'supervisor'

class PasswordResetCode(models.Model):
    #NEW
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

# Crear automáticamente el perfil al crear el usuario
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfilusuario.objects.create(user=instance)