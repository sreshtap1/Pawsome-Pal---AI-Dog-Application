from django.urls import path
from .views import RegisterView, UserView, ChangePasswordView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login', obtain_auth_token),
    path('register', RegisterView.as_view()),
    path('profile/<str:pk>', UserView.as_view()),
    path('profile/changepassword', UserView.as_view()),
]
