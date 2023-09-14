from django.db import models
from account.models import CustomUser
from community.models import Community


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    text = models.TextField(max_length=150, blank=True)

    # date_create

    def __str__(self):
        return f'{self.image}'


class Album(models.Model):
    name = models.CharField(max_length=100)
    # дата создания для сортировки по ней
    avatar_album = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ManyToManyField(Photo, related_name='album_photo', blank=True)

    def __str__(self):
        return f'{self.name}'


class PhotoComment(models.Model):
    text = models.TextField(max_length=500)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'
