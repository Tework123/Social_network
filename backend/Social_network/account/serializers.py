from rest_framework import serializers

from account.models import CustomUser, Education


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
