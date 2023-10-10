from rest_framework import serializers

from community.models import Community


class CommunityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'
