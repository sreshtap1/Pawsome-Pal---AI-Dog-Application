from django.db import models
from django.contrib.auth import get_user_model
import string, random

User = get_user_model()

# Create your models here.


def generateRandomID():
    return "".join([i for i in random.choices(string.ascii_lowercase, k=6)])


class ChatRoom(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    user1 = models.ForeignKey(
        User, related_name='user1', on_delete=models.SET_NULL, null=True)
    user2 = models.ForeignKey(
        User, related_name='user2', on_delete=models.SET_NULL, null=True)
    chat_id = models.CharField(default=generateRandomID, max_length=6)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['user1', 'user2']


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(
        ChatRoom, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp', )