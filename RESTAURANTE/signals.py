from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Cajero, Mesero, Cocinero
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
        
@receiver(post_save, sender=Cajero)
def crear_usuario_cajero(sender, instance, created, **kwargs):
    if created and not instance.usuario:
        user = User.objects.create_user(
            username=instance.pin,
            password=instance.pin,
        )
        print("usuario cajero crear ", instance.pin)
        if hasattr(user, 'role'):
            user.role = "cajero"
            user.save()

        Cajero.objects.filter(id=instance.id).update(usuario=user)
        
@receiver(post_save, sender=Cocinero)
def crear_usuario_cajero(sender, instance, created, **kwargs):
    if created and not instance.usuario:
        user = User.objects.create_user(
            username=instance.pin,
            password=instance.pin,
        )
        print("usuario cocinero crear ", instance.pin)
        if hasattr(user, 'role'):
            user.role = "cocinero"
            user.save()

        Cajero.objects.filter(id=instance.id).update(usuario=user)
