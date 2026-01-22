from channels.generic.websocket import AsyncJsonWebsocketConsumer

class CocinaComandasConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.close(code=4401)
            return

        role = getattr(user, "role", None)
        if role not in ("cocinero", "admin", "supervisor"):
            await self.close(code=4403)
            return
        
        cocinero = getattr(user, "cocinero", None)
        if not cocinero or not cocinero.area_cocina:
            await self.close(code=4403)
            return

        self.group_name = f"cocina_area_{cocinero.area_cocina.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

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