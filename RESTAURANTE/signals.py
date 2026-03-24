from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Cajero, Mesero, Cocinero
from decimal import Decimal, ROUND_HALF_UP
import logging

logger = logging.getLogger(__name__)

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
        
@receiver(post_save, sender=Cajero)
def crear_usuario_cajero(sender, instance, created, **kwargs):
    if created and not instance.usuario:
        user = User.objects.create_user(
            username=instance.pin,
            password=instance.pin,
        )
        logger.info("usuario cajero crear %s", instance.pin)
        if hasattr(user, 'role'):
            user.role = "cajero"
            user.save()

        Cajero.objects.filter(id=instance.id).update(usuario=user)
        
@receiver(post_save, sender=Cocinero)
def crear_usuario_cocinero(sender, instance, created, **kwargs):
    if created and not instance.usuario:
        user = User.objects.create_user(
            username=instance.pin,
            password=instance.pin,
        )
        logger.info("usuario cocinero crear %s", instance.pin)
        if hasattr(user, 'role'):
            user.role = "cocinero"
            user.save()

        Cocinero.objects.filter(id=instance.id).update(usuario=user)
