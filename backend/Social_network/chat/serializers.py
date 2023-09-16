from rest_framework import serializers

from album.models import Photo
from chat.models import Chat, Relationship, Message


# chat
class ChatListSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField('last_message')

    def last_message(self, obj):
        last_message = Message.objects.filter(chat_id=obj.pk).prefetch_related(
            'photo').order_by('-date_create')[:1]
        return MessageChatEditSerializer(last_message, many=True).data

    class Meta:
        model = Chat
        fields = ['id', 'name', 'message']


class ChatEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name', 'user']


# chat message
class MessageChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'date_create', 'date_change', 'user', 'mock', 'photo']


class MessageChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text']


class MessageChatEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'date_create', 'date_change', 'photo']


class MessageMockChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'photo']


# dialogs
class RelationshipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id', 'user_1', 'user_2', 'status']


class RelationshipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id', 'user_2', 'status']


class RelationshipEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id', 'status']


# dialogs message
class MessageRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'date_create', 'date_change', 'user', 'mock', 'photo']


class MessageRelationshipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text']


class MessageRelationshipEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'date_change', 'photo']


class MessageMockRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'photo']
