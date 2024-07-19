from . import views
from django.urls import path

urlpatterns = [
    path('animals', views.AnimalView.as_view()),
    path('animals/<str:pk>', views.AnimalView.as_view()),
    path('animals/<str:animal>/image', views.AnimalImageView.as_view()),
    path('animals/<str:animal>/image/<str:pk>',
         views.AnimalImageView.as_view()),
    path('adoption', views.AdoptionApplicationView.as_view()),
    path('adoption/<str:pk>', views.AdoptionApplicationView.as_view()),
    path('rescue', views.RescueRequestView.as_view()),
    path('rescue/<str:pk>', views.RescueRequestView.as_view())
]
