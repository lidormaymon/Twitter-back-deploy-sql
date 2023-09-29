import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json["text"]
        sender_id = text_data_json["sender_id"]
        timestamp = text_data_json["timestamp"]
        conversation_id = text_data_json["conversation_id"]
        recipient_id = text_data_json['recipient_id']
        image = text_data_json.get("image", None)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "chat.message",
                "text": text,
                "sender_id": sender_id,
                "timestamp": timestamp,
                "conversation_id":conversation_id,
                "recipient_id":recipient_id,
                "image":image
            }
        )   


    # Receive message from room group
    def chat_message(self, event):
        text = event["text"]
        sender_id = event["sender_id"]  
        timestamp = event["timestamp"]
        conversation_id = event['conversation_id']
        recipient_id = event["recipient_id"]
        image = event["image"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(
            {
                "text": text, 
                "sender_id": sender_id,
                "timestamp":timestamp,
                "conversation_id":conversation_id,
                "recipient_id":recipient_id,
                "image":image
            }))
