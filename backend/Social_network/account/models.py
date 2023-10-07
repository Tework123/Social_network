from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from account.managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = PhoneNumberField(unique=False, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    about_me = models.TextField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='photos/', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    date_last_visit = models.DateTimeField(null=True, blank=True)
    date_last_password_reset = models.DateTimeField(null=True, blank=True)
    lifestyle = models.TextField(max_length=1000, blank=True)
    interest = models.TextField(max_length=1000, blank=True)

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'


class Education(models.Model):
    name = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=50, blank=True)
    level = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True)

    # для одного года проще создать еще одно поле,
    # туда записать цифру года, а это оставить? choice написать для выбора года,
    # либо на фронте это можно сделать
    date_graduation = models.DateField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, related_name='education', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Work(models.Model):
    name = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_stop = models.DateField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, related_name='work', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
