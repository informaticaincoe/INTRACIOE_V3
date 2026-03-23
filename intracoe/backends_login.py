import logging
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from RESTAURANTE.models import Cajero, Cocinero, Mesero

logger = logging.getLogger(__name__)

User = get_user_model()

class MultiRoleBackend(BaseBackend): # <--- Asegúrate de este nombre
    def authenticate(self, request, username=None, **kwargs):
        logger.debug(f"DEBUG BACKEND: Recibido PIN {username}")
        if not username:
            return None
        
        # 1. Buscar Mesero
        mesero = Mesero.objects.filter(codigo=username, activo=True).first()
        if mesero and mesero.usuario:
            logger.debug(f"DEBUG: Mesero encontrado: {mesero.nombre}")
            return mesero.usuario

        # 2. Buscar Cocinero
        cocinero = Cocinero.objects.filter(pin=username, activo=True).first()
        if cocinero and cocinero.usuario:
            logger.debug(f"DEBUG: Cocinero encontrado: {cocinero.nombre}")
            return cocinero.usuario
        
        cajero = Cajero.objects.filter(pin=username, activo=True).first()
        if cajero and cajero.usuario:
            logger.debug(f"DEBUG: Cajero encontrado: {cajero.nombre}")
            return cajero.usuario

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None