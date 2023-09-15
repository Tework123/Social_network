from django.db import models
from django.utils import timezone

from account.models import CustomUser
from community.models import Community


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    text = models.TextField(max_length=150, blank=True)
    date_create = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    # date_create

    def __str__(self):
        return f'{self.image}'


class Album(models.Model):
    name = models.CharField(max_length=100)
    date_create = models.DateField(default=timezone.now)
    avatar_album = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ManyToManyField(Photo, related_name='album_photo', blank=True)

    def __str__(self):
        return f'{self.name}'


class PhotoComment(models.Model):
    text = models.TextField(max_length=500)
    date_create = models.DateTimeField(default=timezone.now)
    date_change = models.DateTimeField(blank=True, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.text}'
