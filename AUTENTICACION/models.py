from django.conf import settings
from django.db import models
import uuid

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
    
class Perfilusuario(models.model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} – {self.nombre} {self.apellido}"