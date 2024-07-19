from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.db import models

from .models import AnimalImages, Animal
from accounts.models import User

@receiver(pre_delete, sender=AnimalImages)
def delete_file(sender, instance, **kwargs):
    file_path = instance.image.path
    if default_storage.exists(file_path):
        default_storage.delete(file_path)