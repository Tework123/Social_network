from django.db import models

from account.models import CustomUser


class Community(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}'
