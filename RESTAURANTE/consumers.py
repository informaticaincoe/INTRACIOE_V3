from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class CocinaComandasConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close(code=4401)
            return

        # Obtenemos los datos del usuario de forma segura (asíncrona)
        user_data = await self.get_user_permissions(user)
        
        if not user_data or user_data['role'] not in ("cocinero", "admin", "supervisor"):
            await self.close(code=4403)
            return

        # Si no tiene área (ej. es admin sin área), manejas el nombre del grupo
        if not user_data['area_id']:
            # Podrías unirlos a un grupo 'global' si quieres que vean todo
            self.group_name = "cocina_global"
        else:
            self.group_name = f"cocina_area_{user_data['area_id']}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    @database_sync_to_async
    def get_user_permissions(self, user):
        """
        Esta función corre en un hilo separado donde sí se permite 
        acceder a la base de datos de Django.
        """
        try:
            # Forzamos la carga de los atributos relacionados
            role = getattr(user, "role", None)
            cocinero = getattr(user, "cocinero", None)
            area_id = cocinero.area_cocina.id if cocinero and cocinero.area_cocina else None
            
            return {
                'role': role,
                'area_id': area_id
            }
        except Exception:
            return None

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def comanda_created(self, event):
        await self.send_json({"type": "comanda_created", "comanda": event["comanda"]})
        
class MeseroNotifsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        
        if not user.is_authenticated:
            await self.close(code=4401)
            return
        
        role = getattr(user, "role", None)
        if role != "mesero":
            await self.close(code=4403)
            return
        
        # Grupo por usuario mesero
        self.group_name = f"mesero_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def pedido_listo(self, event):
        await self.send_json({"type": "pedido_listo", "data": event["data"]})