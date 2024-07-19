from rest_framework import generics, permissions, mixins, status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# Create your views here.
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Register a new user in the system."""
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        # Call REST framework's base class to run full validation first
        return self.create(request, *args, **kwargs)


class UserView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer    
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({
                'message': 'User Logout Successfully'
            }, status=204)
        except Exception as e:
            print('Error on logout', str(e))
            return Response({
                'message': str(e)
            }, status=200)
        
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User    

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Your old password doesn't match."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'message': 'Password updated successfully',
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
