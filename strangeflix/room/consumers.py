# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RoomControl
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        if self.user.is_authenticated:
            self.is_member = await self.check_if_member()
            self.is_host = await self.check_if_host()
            if self.is_member or self.is_host:
                # Join room group
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'add_user',
                            'user':self.user.username
                        }
                )
                await self.accept()

    @database_sync_to_async
    def check_if_member(self):
        return self.user in RoomControl.objects.filter(room_id = self.room_name).first().members.all()
    

    @database_sync_to_async
    def check_if_host(self):
        return self.user == RoomControl.objects.filter(room_id = self.room_name).first().host_user

    async def disconnect(self, close_code):
        # Leave room group
        if(hasattr(self,'room_group_name')):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'remove_user',
                            'user':self.user.username
                            
                        }
                )


    # Receive message from WebSocket
    async def receive(self, text_data):
        if self.user.is_authenticated:
            self.is_member = await self.check_if_member()
            self.is_host = await self.check_if_host()
            if self.is_member or self.is_host:
                text_data_json = json.loads(text_data)
                message = text_data_json['message']
                message_type = text_data_json['type']
                # Send message to room group
                if message_type == 'chat_message':
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message,
                            'user':self.user.username
                        }
                )
                if message_type == 'play':
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'play',
                            'message':message,
                            'user':self.user.username
                        }
                    )
                if message_type == 'skip':
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'skip',
                            'message': message,
                            'skipAmount': text_data_json['skipAmount'],
                            'user':self.user.username
                        }
                    )
                if message_type == 'upd':
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type':'upd',
                            'message':message,
                            'updTime':text_data_json['updTime'],
                            'user':self.user.username
                        }
                    )
                if message_type == 'join':
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type':'join',
                            'message':message,
                            'user':self.user.username
                        }
                    )
                if message_type == 'hostupd' and self.is_host:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type':'hostupd',
                            'message':message,
                            'pausedStatus':text_data_json['pausedStatus'],
                            'currentTimeStatus':text_data_json['currentTimeStatus'],
                            'videoStatus':text_data_json['videoStatus'],
                            'users':text_data_json['users'],
                            'user':self.user.username
                        }
                    )
                if message_type == 'close_room':
                    print(hi)
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'close_room',
                            'message': message,
                            'user':self.user.username
                        }
                )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type':'chat_message',
            'message': message,
            'user':event['user']
        }))
    
    #Send play control
    async def play(self,event):
        message = event['message']

        #Send play control to WebSocket
        await self.send(text_data=json.dumps({
            'type':'play',
            'message':message,
            'user':event['user']
        }))

    #Send skip control
    async def skip(self,event):
        message = event['message']
        skipAmount = event['skipAmount']

        #Send skip control to WebSocket
        await self.send(text_data=json.dumps({
            'type':'skip',
            'message':message,
            'skipAmount':skipAmount,
            'user':event['user']
        }))
    
    #Send updated time
    async def upd(self,event):
        message = event['message']
        updTime = event['updTime']

        #Send updated time control to WebSocket
        await self.send(text_data=json.dumps({
            'type':'upd',
            'message':message,
            'updTime':updTime,
            'user':event['user']
        }))

    #Send join request
    async def join(self,event):
        message = event['message']

        #Send join request to WebSocket
        await self.send(text_data=json.dumps({
            'type':'join',
            'message':message,
            'user':event['user']
        }))
    
    #Send host update
    async def hostupd(self,event):
        message = event['message']
        pausedStatus = event['pausedStatus']
        currentTimeStatus = event['currentTimeStatus']
        videoStatus = event['videoStatus']
        users = event['users']
        #Send join request to WebSocket
        await self.send(text_data=json.dumps({
            'type':'hostupd',
            'message':message,
            'pausedStatus': pausedStatus,
            'currentTimeStatus': currentTimeStatus,
            'videoStatus' : videoStatus,
            'users':users,
            'user':event['user']
        }))
    #Send add user
    async def add_user(self,event):
        print(event['user'])
        #Send play control to WebSocket
        await self.send(text_data=json.dumps({
            'type':'add_user',
            'user':event['user']
        }))    

    #Send remove user    
    async def remove_user(self,event):
        #Send play control to WebSocket
        await self.send(text_data=json.dumps({
            'type':'remove_user',
            'user':event['user']
        }))
    
    # Receive host left from room group
    async def close_room(self, event):
        message = event['message']
        # Send host left to WebSocket
        await self.send(text_data=json.dumps({
            'type':'close_room',
            'message': message,
            'user':event['user']
        }))