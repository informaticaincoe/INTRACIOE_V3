from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from RESTAURANTE.models import Cajero, Cocinero, Mesero

User = get_user_model()

class MultiRoleBackend(BaseBackend): # <--- Asegúrate de este nombre
    def authenticate(self, request, username=None, **kwargs):
        print(f"DEBUG BACKEND: Recibido PIN {username}")
        if not username:
            return None
        
        # 1. Buscar Mesero
        mesero = Mesero.objects.filter(codigo=username, activo=True).first()
        if mesero and mesero.usuario:
            print(f"DEBUG: Mesero encontrado: {mesero.nombre}")
            return mesero.usuario

        # 2. Buscar Cocinero
        cocinero = Cocinero.objects.filter(pin=username, activo=True).first()
        if cocinero and cocinero.usuario:
            print(f"DEBUG: Cocinero encontrado: {cocinero.nombre}")
            return cocinero.usuario
        
        cajero = Cajero.objects.filter(pin=username, activo=True).first()
        if cajero and cajero.usuario:
            print(f"DEBUG: Cocinero encontrado: {cajero.nombre}")
            return cajero.usuario

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None