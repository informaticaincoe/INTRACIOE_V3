from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Mesero
from decimal import Decimal, ROUND_HALF_UP

User = get_user_model()

@receiver(post_save, sender=Mesero)
def crear_usuario_mesero(sender, instance, created, **kwargs):
    if created and not instance.usuario:
        user = User.objects.create_user(
            username=instance.codigo,
            password=instance.codigo, # El código sirve de pass inicial
        )
        
        if hasattr(user, 'role'):
            user.role = "mesero"
            user.save()

        Mesero.objects.filter(id=instance.id).update(usuario=user)