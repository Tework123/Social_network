from django.contrib.auth.models import User
from rest_framework import serializers

from login.models import ProfilePhoto


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'],
                                        username=validated_data['email'],
                                        password=validated_data['password'],
                                        is_active=False)
        return user

    class Meta:
        model = User
        fields = ['email', 'password']


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = '__all__'
