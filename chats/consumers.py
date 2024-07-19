from channels.generic.websocket import WebsocketConsumer
import json
from . import models
from django.db.models import Q
from . import serializers
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync

User = get_user_model()


class UserChatConsumer(WebsocketConsumer):
    def connect(self):
        if not self.scope['user'].is_anonymous:
            self.email = self.scope['user'].get_email_username()
            self.room_name = str(self.email).split("@")[0]
            self.room_group_name = f"user_{self.room_name}"

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name)

            self.accept()
            self.set_user_online(True)
            chats = self.get_user_chats()
            # self.send('chats')
            self.send(json.dumps(chats))
        else:
            self.accept()
            self.send(json.dumps({"message": "credentials not provided"}))
            self.close()

    def disconnect(self, code):
        self.set_user_online(False)
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, text_data)

    def chat_operation(self, event):
        value = event['value']
        self.send(json.dumps(value))

    def send_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({"message": message}))

    def get_user_chats(self):
        chats = models.ChatRoom.objects.filter(
            Q(user1=self.scope['user']) | Q(user2=self.scope['user']))
        data = serializers.ChatRoomSerializer(chats, many=True).data

        return data

    def set_user_online(self, status):
        User.set_user_online(self.scope['user'], status)


class MessageChatConsumer(WebsocketConsumer):
    def connect(self):
        if not self.scope['user'].is_anonymous:
            self.room_name = self.scope["url_route"]["kwargs"]["chat_room"]
            self.room_group_name = f"room_{self.room_name}"

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name)

            self.accept()

            self.chat_room = self.get_chat_object()

            if self.chat_room == None:
                # If the room doesn't exist then close the connection
                # self.accept()
                self.send(json.dumps({"message": "Chat room doesn't exists"}))
                self.close()
                return

            messages = self.get_user_messages()
            self.send(json.dumps(messages))
        else:
            self.accept()
            self.send(json.dumps({"message": "credentials not provided"}))
            self.close()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, text_data)

    def message_operation(self, event):
        value = event['value']
        self.send(json.dumps(value))

    def add_message(self, event):
        message = event['message']
        self.add_user_message(message)

    def get_chat_object(self):
        try:
            obj = models.ChatRoom.objects.get(chat_id=self.room_name)
            return obj
        except Exception as e:
            return None

    def get_user_messages(self):
        messages = models.Message.objects.filter(
            chat_room=self.chat_room).order_by('-timestamp')
        data = serializers.MessageSeriliazer(messages, many=True).data

        return data

    def add_user_message(self, data):
        data['user'] = self.scope['user']
        data['chat_room'] = self.chat_room
        
        try:
            message = models.Message(
                user=data['user'], chat_room=data['chat_room'], content=data['content'])
            message.save()
        except Exception as e:
            print(e)
