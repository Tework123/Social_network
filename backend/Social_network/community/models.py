from django.db import models


class Community(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey('CustomUser', on_delete=models.PROTECT)
