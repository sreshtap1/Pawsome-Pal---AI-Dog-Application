from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . import models, serializers
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=models.ChatRoom)
def add_chat(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    data = serializers.ChatRoomSerializer(instance).data

    async_to_sync(channel_layer.group_send)(
        f"user_{instance.user1.get_email_username()}", {
            'type': 'chat.operation',
            'value': {
                "action": "add",
                "room": data
            }
        })

    async_to_sync(channel_layer.group_send)(
        f"user_{instance.user2.get_email_username()}", {
            'type': 'chat.operation',
            'value': {
                "action": "add",
                "room": data
            }
        })


@receiver(post_delete, sender=models.ChatRoom)
def delete_chat(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    data = serializers.ChatRoomSerializer(instance).data

    async_to_sync(channel_layer.group_send)(
        f"user_{instance.user1.get_email_username()}", {
            'type': 'chat.operation',
            'value': {
                "action": "remove",
                "room": data
            }
        })

    async_to_sync(channel_layer.group_send)(
        f"user_{instance.user2.get_email_username()}", {
            'type': 'chat.operation',
            'value': {
                "action": "remove",
                "room": data
            }
        })


@receiver([post_save], sender=models.Message)
def add_message(sender, instance, **kwargs):
    channel_layer = get_channel_layer()    
    # print("Add Called")

    data = serializers.MessageSeriliazer(instance).data
    room_id = instance.chat_room.chat_id

    async_to_sync(channel_layer.group_send)(
        f"room_{room_id}", {
            "type": "message.operation",
            "value": {
                "action": "add",
                "message": data
            }
        }
    )


@receiver(post_delete, sender=models.Message)
def delete_message(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    print("Delete Called")

    data = serializers.MessageSeriliazer(instance).data
    room_id = instance.chat_room.chat_id

    async_to_sync(channel_layer.group_send)(
        f"room_{room_id}", {
            "type": "message.operation",
            "value": {
                "action": "remove",
                "message": data
            }
        }
    )
