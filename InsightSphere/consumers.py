import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        await self.accept()
        await self.channel_layer.group_add(
            self.channel_id,
            self.channel_name
        )
        

        await self.channel_layer.group_send(
            self.channel_id,
            {
                'type': 'msg.server',
                'username': self.scope['user'].username,
                'rec': 'Entrou do chat. 😄👋'
            }
            )


    async def msg_server(self, event):
            
        await self.send(text_data=json.dumps({
            'msgserver': f"{event['username']} {event['rec']}",
            'type':'msg.server'
        }))

        
    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.channel_id,
            {
                'type': 'msg.server',
                'username': self.scope['user'].username,
                'rec': 'Saiu do chat.'
            }
        )
        await self.channel_layer.group_discard(
            self.channel_id,
            self.channel_name
        )


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        apelido = data['apelido']
        username = data['username']
        hora = data['hora']

        await self.channel_layer.group_add(
            self.channel_id,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.channel_id,
            {
                'type': 'chat.message',
                'message': message,
                'apelido': apelido,
                'username': username,
                'hora': hora
            }
        )

    async def chat_message(self, event):
        message = event['message']
        apelido = event['apelido']
        username = event['username']
        hora = event['hora']

        await self.send(text_data=json.dumps({
            'message': message,
            'apelido': apelido,
            'username': username,
            'hora': hora
        }))