from rest_framework import serializers

from chat.models import Chat, Relationship, Message


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'user']


class ChatEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'user']


class RelationshipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id', 'user_1', 'user_2', 'status']


class RelationshipEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id', 'status']


class MessageChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'date_create', 'date_change', 'user']


class MessageChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'date_create', 'date_change']


class MessageChatEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'date_change']
