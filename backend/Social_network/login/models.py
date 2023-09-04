from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, Group, PermissionsMixin
from django.db import models
from django.db.models import DateField
from phonenumber_field.modelfields import PhoneNumberField

from login.managers import UserManager


# изменяем стандартную модель юзера
# User._meta.get_field('email')._unique = True
# User._meta.get_field('email')._blank = False


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'password']

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=40, unique=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    date_of_birth = DateField(null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'


class ProfilePhoto(models.Model):
    photo = models.ImageField(upload_to='photos/')
