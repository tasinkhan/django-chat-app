import json
import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize room_group_name with None to ensure the attribute always exists
        self.room_group_name = None
        self.room_name = None

    async def connect(self):
        user = self.scope["user"]
        
        if user.is_authenticated:
            try:
                # Get the organization using database_sync_to_async
                organization = await self.get_organization(user)
                
                # Set room name and group name
                self.room_name = organization.name
                self.room_group_name = f"chat_{self.room_name}"
                
                print("===user====", self.scope["user"])
                
                # Join the room group
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                
                # Accept the WebSocket connection
                await self.accept()
            except Exception as e:
                print(f"Error during connection: {e}")
                await self.close()
        else:
            await self.close()
        
    async def disconnect(self, close_code):
        if hasattr(self, 'channel_layer') and self.room_group_name:
            try:
                await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
                print(f"User disconnected from {self.room_group_name}")
            except Exception as e:
                print(f"Error during disconnect: {e}")

    @database_sync_to_async
    def get_username(self, user):
        return user.username

    @database_sync_to_async
    def get_organization(self, user):
        return user.organization

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
