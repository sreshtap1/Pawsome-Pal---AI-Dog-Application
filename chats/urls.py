from django.urls import path
from . import views

urlpatterns = [
    path('chat', views.ChatRoomView.as_view()),
    path('chat/<str:pk>', views.ChatRoomView.as_view()),
]
