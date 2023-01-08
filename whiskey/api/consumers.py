import json
from channels.generic.websocket import WebsocketConsumer


class WhiskeyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_node):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        self.send(text_data=json.dumps({"message": data["message"]}))
