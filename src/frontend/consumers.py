import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BookingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Отримуємо ID сеансу з URL (той самий session_id з routing.py)
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'booking_{self.session_id}'

        # Приєднуємо користувача до групи цього конкретного залу
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Видаляємо користувача з групи при відключенні
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get('action') == 'reserve':
            # Шлемо повідомлення всій групі
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'seats_reserved', # Це викликає метод нижче
                    'seats': data['seats'],
                    'action': 'reserve'
                }
            )

    async def seats_reserved(self, event):
        # Цей метод спрацьовує у кожного користувача в групі
        await self.send(text_data=json.dumps({
            'action': event['action'],
            'seats': event['seats']
        }))