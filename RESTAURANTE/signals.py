from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Mesero

User = get_user_model()

@receiver(post_save, sender=Mesero)
def crear_usuario_mesero(sender, instance, created, **kwargs):
    if created and not instance.usuario:
        # 1. Crear el usuario de Django
        # El username será el código para que sea único
        user = User.objects.create_user(
            username=instance.codigo,
            password=instance.codigo, # El código sirve de pass inicial
        )
        # Si tu modelo User tiene el campo role, lo asignamos
        if hasattr(user, 'role'):
            user.role = "mesero"
            user.save()

        # 2. Vincular usando update para NO disparar post_save de nuevo
        Mesero.objects.filter(id=instance.id).update(usuario=user)
