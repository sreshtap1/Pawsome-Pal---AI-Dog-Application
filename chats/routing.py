from channels.routing import URLRouter
from django.urls import path
from . import consumers

ws_patterns = URLRouter([
    path('chat', consumers.UserChatConsumer.as_asgi()),
    path('message/<str:chat_room>', consumers.MessageChatConsumer.as_asgi()),
])
