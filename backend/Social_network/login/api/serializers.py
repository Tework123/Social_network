from rest_framework import serializers
from account.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class RegisterTrySerializer(serializers.Serializer):
    email = serializers.EmailField()


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ResetPasswordSendEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class ResetPasswordCreatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
