from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        fields = ['id', 'email', 'first_name', 'last_name',
                  'phone', 'city', 'about_me', 'avatar',
                  'date_of_birth', 'date_joined', 'date_last_visit',
                  'date_last_password_reset', 'lifestyle', 'interest', 'education', 'work']


class AccountEditSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        attrs._mutable = True

        if not attrs['date_of_birth']:
            attrs['date_of_birth'] = None

        return attrs

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'phone', 'city', 'about_me', 'avatar',
                  'date_of_birth', 'lifestyle', 'interest']


class AccountEditEducationSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs._mutable = True

        if attrs['name'] == '':
            raise ValidationError('Название учебного заведения должно быть заполнено')

        if not attrs['date_graduation']:
            attrs['date_graduation'] = None

        return attrs

    class Meta:
        model = Education
        fields = ['id', 'name', 'city', 'level', 'status', 'date_graduation']
