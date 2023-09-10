from django.db import models
from account.models import CustomUser
from chat.models import Message
from community.models import Community
from post.models import Post


class Album(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)

    # @property
    # def photo(self):
    #     print(123)
    #     print(123)
    #     print(123)
    #     print(123)
    #
    #     return '123'

    def __str__(self):
        return f'{self.name}'


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    text = models.TextField(max_length=150, blank=True)
    # date_create
    album = models.ForeignKey(Album, related_name='photo', on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, related_name='photo', on_delete=models.CASCADE, blank=True, null=True)
    message = models.ForeignKey(Message, related_name='photo', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.image}'


class PhotoComment(models.Model):
    text = models.TextField(max_length=500)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'
