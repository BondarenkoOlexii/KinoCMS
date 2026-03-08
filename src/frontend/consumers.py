import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BookingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'booking_{self.session_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get('action') == 'reserve':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'seats_reserved',
                    'seats': data['seats'],
                    'action': 'reserve'
                }
            )

    async def seats_reserved(self, event):
        await self.send(text_data=json.dumps({
            'action': event['action'],
            'seats': event['seats']
        }))