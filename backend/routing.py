from chats.routing import ws_patterns as chat_patterns
from channels.routing import URLRouter
from django.urls import path

ws_patterns = URLRouter([
    path("api-chat/", chat_patterns)
])
