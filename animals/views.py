from rest_framework import permissions, generics, mixins
from rest_framework.response import Response
from . import serializers, models
# Create your views here.


class AnimalView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = serializers.AnimalSerializer    
    queryset = models.Animal.objects.all()

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AnimalImageView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = serializers.AnimalImagesSerializers    
    queryset = models.AnimalImages.objects.all()

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)

        if 'animal' in kwargs:
            images = models.AnimalImages.objects.filter(
                animal=kwargs['animal'])
            data = self.serializer_class(images, many=True).data
            return Response(data, 200)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AdoptionApplicationView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = serializers.AdoptionApplicationSerializer    
    queryset = models.AdoptionApplication.objects.all()

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)

        applications = models.AdoptionApplication.objects.filter(
            applicant=request.user)
        s = self.serializer_class(applications, many=True).data

        return Response(s, 200)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RescueRequestView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = serializers.RescueRequestSerializer    
    queryset = models.RescuedTable.objects.all()

    def get(self, request, *args, **kwargs):

        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)

        requests = models.RescuedTable.objects.filter(rescuer=request.user)
        data = self.serializer_class(requests, many=True).data

        return Response(data, 200)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
