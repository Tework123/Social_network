from django.contrib.auth.models import User
from rest_framework import serializers

from login.models import ProfilePhoto, CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class ResetPasswordSendEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class ResetPasswordCreatePasswordSerializer(serializers.ModelSerializer):
    # confirm_password = serializers.CreateOnlyDefault

    class Meta:
        model = CustomUser
        fields = ['password']
