from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Perfilusuario

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_profile(sender, instance, created, **kwargs):
    if not hasattr(instance, "perfilusuario"):
        Perfilusuario.objects.get_or_create(user=instance)
