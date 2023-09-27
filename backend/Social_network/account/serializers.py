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
    # def validate(self, attrs):
    #     # attrs._mutable = True
    #
    #     # if not attrs['date_of_birth']:
    #     #     attrs['date_of_birth'] = None

    #
    #     return attrs

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'phone', 'city', 'about_me',
                  'date_of_birth', 'lifestyle', 'interest']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': True},
            'city': {'required': True},
            'about_me': {'required': True},
            'date_of_birth': {'required': True},
            'lifestyle': {'required': True},
            'interest': {'required': True},

        }


class AccountEditAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['avatar']
        extra_kwargs = {
            'avatar': {'required': True}
        }


class AccountEditEducationSerializer(serializers.ModelSerializer):
    # def validate(self, attrs):
    #     attrs._mutable = True
    #
    #     if attrs['name'] == '':
    #         raise ValidationError('Название учебного заведения должно быть заполнено')
    #
    #     if not attrs['date_graduation']:
    #         attrs['date_graduation'] = None
    #
    #     return attrs

    class Meta:
        model = Education
        fields = ['id', 'name', 'city', 'level', 'status', 'date_graduation']
        extra_kwargs = {
            'name': {'required': True},
            'city': {'required': True},
            'level': {'required': True},
            'status': {'required': True},
            'date_graduation': {'required': True},
        }


class AccountEditWorkSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        # attrs._mutable = True
        #
        # if attrs['name'] == '':
        #     raise ValidationError('Название места работы должно быть заполнено')
        #
        # if not attrs['date_start']:
        #     attrs['date_start'] = None
        # #
        # if not attrs['date_stop']:
        #     attrs['date_stop'] = None

        if attrs['date_start'] and attrs['date_stop']:
            if attrs['date_start'] > attrs['date_stop']:
                raise ValidationError('Дата начала работы должна быть позже даты конца')

        return attrs

    class Meta:
        model = Work
        fields = ['id', 'name', 'city', 'status', 'date_start', 'date_stop']
        extra_kwargs = {
            'name': {'required': True},
            'city': {'required': True},
            'status': {'required': True},
            'date_start': {'required': True},
            'date_stop': {'required': True},
        }
