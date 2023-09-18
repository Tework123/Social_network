from django.db import models
from account.models import CustomUser
from album.models import Photo
from community.models import Community


class Post(models.Model):
    text = models.TextField(max_length=5000, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ManyToManyField(Photo, related_name='post_photo', blank=True)

    def __str__(self):
        return f'{self.text}'
