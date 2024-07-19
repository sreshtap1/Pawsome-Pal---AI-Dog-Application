from rest_framework import serializers
from . import models
from accounts.serializers import UserSerializer


class AnimalImagesSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.AnimalImages
        fields = ('id', 'image', 'uploaded_date', 'animal', 'uploaded_by')
        extra_kwargs = {'animal': {'write_only': True},
                        'uploaded_by': {'write_only': True}}


class AnimalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, source="registered_by")
    images = AnimalImagesSerializers(many=True, read_only=True)

    class Meta:
        model = models.Animal
        fields = ('id', 'name', 'animal_type', 'age', 'breed', 'gender', 'description',
                  'status', 'animal_profile', 'registered_by', 'user', 'registered_on', 'images')
        extra_kwargs = {'registered_by': {'write_only': True}}


class AdoptionApplicationSerializer(serializers.ModelSerializer):
    application_animal = AnimalSerializer(read_only=True, source="animal")

    class Meta:
        model = models.AdoptionApplication
        fields = ('id', 'applicant', 'animal',
                  'application_animal', 'application_date', 'status', 'reason')
        extra_kwargs = {'applicant': {'write_only': True},
                        'animal': {'write_only': True}}

    def validate(self, attrs):
        application = models.AdoptionApplication.objects.filter(
            applicant=attrs['applicant'], animal=attrs['animal']).exclude(status="Rejected")

        if len(application) > 0:
            raise serializers.ValidationError(
                {"animal": "You have already applied for this pet."})

        return super().validate(attrs)


class RescueRequestSerializer(serializers.ModelSerializer):
    rescue_animal = AnimalSerializer(read_only=True, source="animal")

    class Meta:
        model = models.RescuedTable
        fields = ("animal", "rescue_animal",
                  "rescuer", "status", "rescue_time", "location", "reason")
        extra_kwargs = {'animal': {'write_only': True}}

    def validate(self, attrs):
        # Check whether the rescuer has already made a request to rescue an animal
        requests = models.RescuedTable.objects.filter(animal=attrs['animal'])

        if len(requests) != 0:
            raise serializers.ValidationError(
                {"rescuer": "You have already made a rescue request for this animal."})

        return super().validate(attrs)
