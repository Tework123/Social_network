from rest_framework import serializers

from chat.models import Chat


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['name', 'user']


class ChatEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['name', 'user']