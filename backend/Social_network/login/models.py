from django.contrib.auth.models import User
from django.db import models

# изменяем стандартную модель юзера
User._meta.get_field('email')._unique = True
User._meta.get_field('email')._blank = False
