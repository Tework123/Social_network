from django.contrib.auth.models import User
from rest_framework import serializers

from login.models import ProfilePhoto, CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):

    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(email=validated_data['email'],
    #                                           password=validated_data['password'],
    #                                           is_active=False)
    #     return user

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = '__all__'
