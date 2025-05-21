import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs

from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser


@sync_to_async
def get_user_from_id(user_id):
    try:
        User = get_user_model()  # ✅ burada olmalı
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        from django.contrib.auth.models import AnonymousUser
        return AnonymousUser()



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print("📡 Oda ismi:", self.room_group_name)

        print("🚀 Yeni WebSocket bağlantısı")

        query_string = self.scope['query_string'].decode()
        print("🔍 query_string:", query_string)

        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]
        print("🔐 token:", token)

        if token is None:
            print("❌ Token yok. Kapatılıyor.")
            await self.close()
            return

        try:
            validated_token = AccessToken(token)
            print("✅ Token doğrulandı")
            user_id = validated_token['user_id']
            print("👤 user_id:", user_id)

            self.scope['user'] = await get_user_from_id(user_id)
            print("✅ Kullanıcı bulundu:", self.scope['user'])

        except Exception as e:
            print("🚨 TOKEN HATASI:", e)
            await self.close()
            return


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("✅ Bağlantı kabul edildi")

    async def disconnect(self, close_code):
        # Güvenli kontrol ekledik
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        print("📩 receive() tetiklendi")
        print("📦 Gelen veri:", text_data)

        try:
            data = json.loads(text_data)
            message = data.get('message', '')
            print("💬 Mesaj:", message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except json.JSONDecodeError as e:
            print("❌ JSON FORMAT HATASI:", e)
            await self.close()
        except Exception as e:
            print("❌ receive() GENEL HATA:", e)
            await self.close()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
