from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Mesero

User = get_user_model()

@receiver(post_save, sender=Mesero)
def crear_usuario_mesero(sender, instance, created, **kwargs):
    if created and instance.usuario is None:
        # Crear USER (no Perfilusuario)
        user = User.objects.create_user(
            username=instance.codigo,
            password=instance.codigo,  # contraseña temporal
            role="mesero"
        )

        # Vincular con mesero
        instance.usuario = user
        instance.save()
