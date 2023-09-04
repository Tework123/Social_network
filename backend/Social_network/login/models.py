from django.contrib.auth.models import User
from django.db import models

# изменяем стандартную модель юзера
User._meta.get_field('email')._unique = True
User._meta.get_field('email')._blank = False


# украсть кастомного юзера
# надо еще потом его зарегать кажется

class ProfilePhoto(models.Model):
    photo = models.ImageField(upload_to='photos/')
