from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100)
    custom_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    community = models.ForeignKey('Community', on_delete=models.CASCADE)


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    text = models.TextField(max_length=150, blank=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)


class PhotoComment(models.Model):
    text = models.TextField(max_length=500)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE)
