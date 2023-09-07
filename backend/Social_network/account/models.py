from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from account.managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'password']

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    about_me = models.TextField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='photos/')
    date_of_birth = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_last_visit = models.DateTimeField(null=True, blank=True)
    date_last_password_reset = models.DateTimeField(null=True, blank=True)
    lifestyle = models.TextField(max_length=1000, blank=True)
    interest = models.TextField(max_length=1000, blank=True)

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'


class Education(models.Model):
    city = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=30)
    status = models.CharField(max_length=30, blank=True)
    date_graduation = models.DateTimeField(null=True, blank=True)
    custom_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)


class Work(models.Model):
    city = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=30, blank=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_stop = models.DateTimeField(null=True, blank=True)
    custom_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
