from rest_framework import serializers
from . import models
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('id', 'post', 'author', 'content', 'date')


class CommunityPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = models.CommunityPost
        fields = ('id', 'title', 'content', 'author', 'date', 'comments')


class EducationContentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, source="creator")

    class Meta:
        model = models.EducationContent
        fields = ('id', 'title', 'description', 'category',
                  'upload_date', 'creator', 'author')
        extra_kwargs = {'creator': {'write_only': True}}


class FeedbackSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True, source="user")

    class Meta:
        model = models.Feedback
        fields = ('id', 'creator', 'user', 'message', 'submitted')
        extra_kwargs = {'user': {'write_only': True}}

