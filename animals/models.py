from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


def upload_animal_image(instance, filename):
    return 'user_{0}/animals/{1}'.format(instance.registered_by.id, filename)


adoption_status = (
    ('Available', 'Available'),
    ('Pending', 'Pending'),
    ('Adopted', 'Adopted'),
)


class Animal(models.Model):
    name = models.CharField(max_length=255)
    animal_type = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=255, choices=adoption_status, default='Available')
    animal_profile = models.FileField(upload_to=upload_animal_image, null=True)
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " ("+self.gender+")"


def upload_multiple_animal_images(instance, filename):
    return 'user_{0}/animals/images/{1}'.format(instance.animal.registered_by.id, filename)


class AnimalImages(models.Model):
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="images")
    image = models.FileField(upload_to=upload_multiple_animal_images)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Additional Image for the Animal"
        verbose_name_plural = "Additional Images for the Animals"


application_status = (
    ('Submitted', 'Submitted'),
    ('In Review', 'In Review'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)


class AdoptionApplication(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now=True)
    status = models.CharField(
        max_length=256, choices=application_status, default="Submitted")
    reason = models.TextField()


rescue_status = (
    ('Submitted', 'Submitted'),
    ('Pending', 'Pending'),
    ('Rescued', 'Rescued')
)


class RescuedTable(models.Model):
    animal = models.OneToOneField(
        Animal, on_delete=models.CASCADE, primary_key=True)
    rescuer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=255, choices=rescue_status, default="Submitted")
    rescue_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=256, blank=True)
    reason = models.TextField()


class AnimalBehaviour(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    behaviour = models.CharField(max_length=255)
    analysis_date = models.DateTimeField(auto_now_add=True)
    temperament_score = models.PositiveIntegerField()
