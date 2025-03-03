from django.db import models
from django.utils import timezone
from datetime import timedelta

class Token_data(models.Model):
    nit_empresa = models.CharField(max_length=20, unique=True)  # NIT de la empresa
    password_hacienda = models.CharField(max_length=255)  # Contraseña en texto plano
    password_privado = models.CharField(max_length=255, default="1")
    token = models.CharField(max_length=255, blank=True, null=True)
    token_type = models.CharField(max_length=50, default='Bearer')
    roles = models.JSONField(default=list)  # Almacena los roles como una lista JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # #nuevos campos
    activado = models.BooleanField(default=False, null=True) # Indica si el token ha sido activado
    fecha_caducidad = models.DateTimeField(default=timezone.now, null=True) # Fecha de expiración del token
    def __str__(self):
        return f"Token Data para {self.nit_empresa}"
    
    def save(self, *args, **kwargs):
        # Si es un nuevo registro, calcula la fecha de caducidad
        if not self.pk:
            self.fecha_caducidad = timezone.now() + timedelta(days=1)  # 24 horas

        # Desactivar el token anterior de la empresa
        Token_data.objects.filter(nit_empresa=self.nit_empresa, activado=True).update(activado=False)

        # Asegurar que el nuevo token se guarde como activado
        self.activado = True  

        super(Token_data, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Token Data"
        verbose_name_plural = "Token Data"

