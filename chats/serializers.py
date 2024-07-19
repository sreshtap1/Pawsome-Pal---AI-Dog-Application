from rest_framework import serializers
from . import models
from accounts.serializers import UserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatRoom
        fields = ('id', 'name', 'user1', 'user2', 'description', 'chat_id')


class MessageSeriliazer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, source='user')

    class Meta:
        model = models.Message
        fields = ('id', 'author', 'user', 'content', 'chat_room', 'timestamp')
        extra_kwargs = {'user': {'write_only': True}}
