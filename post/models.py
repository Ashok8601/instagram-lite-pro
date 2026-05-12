from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    title = models.CharField(max_length=100)

    content = models.TextField()

    likes_count = models.IntegerField(default=0)

    comments_count = models.IntegerField(default=0)

    posted_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )
    video = models.FileField(
        upload_to='posts/',
        blank=True,
        null=True
    )
    def __str__(self):
        return self.title

class Reel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reels'

    )
    title = models.CharField(max_length=100)
    caption = models.TextField()
    hashtag = models.CharField(max_length=100, null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    video = models.FileField(
        upload_to='reels/',
    )
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

