from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from account.models import CustomUser, Education, Work


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)
    work = WorkSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'pk', 'email', 'first_name', 'last_name',
                  'phone', 'city', 'about_me', 'avatar',
                  'date_of_birth', 'date_joined', 'date_last_visit',
                  'date_last_password_reset', 'lifestyle', 'interest', 'education', 'work']


class AccountEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'pk', 'first_name', 'last_name',
                  'phone', 'city', 'about_me', 'avatar',
                  'date_of_birth', 'lifestyle', 'interest']










