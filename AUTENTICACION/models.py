from django.conf import settings
from django.db import models
import uuid

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
    codigo = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    url_endpoint = models.URLField(max_length=200, blank=True, null=True)
    ruta_archivo = models.CharField(max_length=100, blank=True, null=True)
    contraseña = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.codigo}"