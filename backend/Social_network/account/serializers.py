from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import CustomUser, Education, Work


class EducationGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'name', 'city', 'level', 'status', 'date_graduation']


class WorkGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['id', 'name', 'city', 'status', 'date_start', 'date_stop']


class CustomUserSerializer(serializers.ModelSerializer):
    education = EducationGETSerializer(many=True)
    work = WorkGETSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name',
                  'phone', 'city', 'about_me', 'avatar',
                  'date_of_birth', 'date_joined', 'date_last_visit',
                  'date_last_password_reset', 'lifestyle', 'interest', 'education', 'work']


class CustomUserEditGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'phone', 'city', 'about_me',
                  'date_of_birth', 'lifestyle', 'interest']


class CustomUserEditPATCHSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
                  'phone', 'city', 'about_me',
                  'date_of_birth', 'lifestyle', 'interest']


class CustomUserEditAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['avatar']
        extra_kwargs = {
            'avatar': {'required': True}
        }


class EducationPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['name', 'city', 'level', 'status', 'date_graduation']


class WorkPOSTSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['date_start'] and attrs['date_stop']:
            if attrs['date_start'] > attrs['date_stop']:
                raise ValidationError('Дата начала работы должна быть позже даты конца')
        return attrs

    class Meta:
        model = Work
        fields = ['name', 'city', 'status', 'date_start', 'date_stop']
