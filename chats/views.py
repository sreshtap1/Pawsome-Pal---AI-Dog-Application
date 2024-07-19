from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from . import models, serializers
from django.db.models import Q

# Create your views here.


class ChatRoomView(generics.CreateAPIView, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = serializers.ChatRoomSerializer
    queryset = models.ChatRoom.objects.all()

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)

        chats = models.ChatRoom.objects.filter(
            Q(user1=request.user) | Q(user2=request.user))
        data = self.serializer_class(chats, many=True).data

        return Response(data, 200)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
