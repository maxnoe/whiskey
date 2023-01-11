from channels.generic.websocket import AsyncWebsocketConsumer



class WhiskeyConsumer(AsyncWebsocketConsumer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def connect(self):
        await self.channel_layer.group_add("whiskey", self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        await self.channel_layer.group_send("whiskey", {"type": "update"})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("whiskey", self.channel_name)

    async def update(self, event):
        await self.send(text_data="update")
