# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(self.user)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message_type = text_data_json['type']
        # Send message to room group
        if message_type == 'chat_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
        )
        if message_type == 'play':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'play',
                    'message':message
                }
            )
        if message_type == 'skip':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'skip',
                    'message': message,
                    'skipAmount': text_data_json['skipAmount']
                }
            )
        if message_type == 'upd':
            print("upd")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'upd',
                    'message':message,
                    'updTime':text_data_json['updTime']
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type':'chat_message',
            'message': message
        }))
    
    #Send play control
    async def play(self,event):
        message = event['message']

        #Send play control to WebSocket
        await self.send(text_data=json.dumps({
            'type':'play',
            'message':message
        }))

    #Send skip control
    async def skip(self,event):
        message = event['message']
        skipAmount = event['skipAmount']

        #Send skip control to WebSocket
        await self.send(text_data=json.dumps({
            'type':'skip',
            'message':message,
            'skipAmount':skipAmount
        }))
    
    #Send updated time
    async def upd(self,event):
        message = event['message']
        updTime = event['updTime']

        #Send updated time control to WebSocket
        await self.send(text_data=json.dumps({
            'type':'upd',
            'message':message,
            'updTime':updTime
        }))