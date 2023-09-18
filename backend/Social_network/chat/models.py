from django.db import models
from account.models import CustomUser
from album.models import Photo


class Chat(models.Model):
    name = models.CharField(max_length=50)
    open_or_close = models.BooleanField(default=False)
    user = models.ManyToManyField(CustomUser)

    # нужен создатель чата, он по умолчанию администратор
    # надо many_to_many для администратора, чтобы можно было
    # их добавлять

    def __str__(self):
        return f'{self.name}'


class Relationship(models.Model):
    user_1 = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='user_1')
    user_2 = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='user_2')
    status = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user_1}, {self.user_2}'


class Message(models.Model):
    text = models.TextField(max_length=2000, blank=True)
    date_create = models.DateTimeField(blank=True, null=True)
    date_change = models.DateTimeField(blank=True, null=True)
    mock = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True, null=True)
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    photo = models.ManyToManyField(Photo, related_name='message_photo', blank=True)

    def __str__(self):
        return f'{self.text}, {self.user}'
