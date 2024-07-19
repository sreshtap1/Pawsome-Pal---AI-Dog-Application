from django.urls import path
from . import views

urlpatterns = [
    path('community', views.CommunityPostView.as_view()),
    path('community/<str:pk>', views.CommunityPostView.as_view()),
    path('community/<str:post>/comment', views.CommentView.as_view()),
    path('community/<str:post>/comment/<str:pk>',
         views.CommentView.as_view()),
]
