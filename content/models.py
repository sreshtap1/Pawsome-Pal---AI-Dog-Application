from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class CommunityPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " by " + str(self.author)


class Comment(models.Model):
    post = models.ForeignKey(
        CommunityPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='replies')  # for nested comments

    class Meta:
        ordering = ['date']


class EducationContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField(verbose_name="Resource Link", blank=True)
    category = models.CharField(max_length=256)
    upload_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return self.title + " | Created by: " + str(self.creator)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    submitted = models.DateField(auto_now_add=True)


class AppContent(models.Model):
    page_title = models.CharField(max_length=100)
    page_content = models.TextField()
    page_upload_date = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.page_title
