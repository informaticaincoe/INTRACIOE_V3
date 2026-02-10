from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import Cocinero, Mesero

User = get_user_model()

class MeseroCodeBackend(BaseBackend):
    """
    Autentica SOLO meseros por su 'codigo' (sin contraseña).
    - Si el mesero no tiene usuario creado, lo crea automáticamente.
    """
    def authenticate(self, request, codigo=None, **kwargs):
        if not codigo:
            return None

        codigo = str(codigo).strip()

        try:
            mesero = Mesero.objects.select_related("usuario").get(codigo=codigo, activo=True)
        except Mesero.DoesNotExist:
            return None

        # Si no hay usuario ligado, lo creamos (opcional pero práctico)
        if not mesero.usuario:
            user = User.objects.create(
                username=codigo,      # puedes usar "MESERO-"+codigo si prefieres
                role="mesero",
                is_active=True,
            )
            user.set_unusable_password()  # importante: no login con password
            user.save()

            mesero.usuario = user
            mesero.save(update_fields=["usuario"])
        else:
            user = mesero.usuario
            if not user.is_active:
                return None
            # Asegurar rol
            if getattr(user, "role", None) != "mesero":
                user.role = "mesero"
                user.save(update_fields=["role"])

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class CocineroPinBackend(BaseBackend):
    """
    Autentica SOLO cocineros por su 'pin' (sin contraseña).
    - Si el cocinero no tiene usuario creado, lo crea automáticamente.
    """
    def authenticate(self, request, pin=None, **kwargs):
        print(">>> CocineroPinBackend llamado con pin:", pin)
        if not pin:
            return None

        pin = str(pin).strip()

        try:
            cocinero = Cocinero.objects.select_related("usuario").get(pin=pin, activo=True)
        except Cocinero.DoesNotExist:
            return None

        if not cocinero.usuario:
            user = User.objects.create(
                username=pin,   # puedes usar "COC-"+pin si prefieres
                role="cocinero",
                is_active=True,
            )
            user.set_unusable_password()
            user.save()

            cocinero.usuario = user
            cocinero.save(update_fields=["usuario"])
        else:
            user = cocinero.usuario
            if not user.is_active:
                return None
            if getattr(user, "role", None) != "cocinero":
                user.role = "cocinero"
                user.save(update_fields=["role"])

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
        
class CocineroPinBackend(BaseBackend):
    """
    Autentica SOLO cocineros por su 'pin' (sin contraseña).
    - Si el cocinero no tiene usuario creado, lo crea automáticamente.
    """
    def authenticate(self, request, pin=None, **kwargs):
        print(">>> CocineroPinBackend llamado con pin:", pin)
        if not pin:
            return None

        pin = str(pin).strip()

        try:
            cocinero = Cocinero.objects.select_related("usuario").get(pin=pin, activo=True)
        except Cocinero.DoesNotExist:
            return None

        if not cocinero.usuario:
            user = User.objects.create(
                username=pin,   # puedes usar "COC-"+pin si prefieres
                role="cocinero",
                is_active=True,
            )
            user.set_unusable_password()
            user.save()

            cocinero.usuario = user
            cocinero.save(update_fields=["usuario"])
        else:
            user = cocinero.usuario
            if not user.is_active:
                return None
            if getattr(user, "role", None) != "cocinero":
                user.role = "cocinero"
                user.save(update_fields=["role"])

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None