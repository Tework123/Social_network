from rest_framework import serializers, exceptions

from album.models import Photo
from chat.models import Chat, Relationship, Message


# chat
class ChatListSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField('last_message')

    def last_message(self, obj):
        # print(3)
        last_message = Message.objects.filter(chat_id=obj.pk).prefetch_related(
            'photo').order_by('-date_create')[:1]
        return MessageChatEditSerializer(last_message, many=True).data

    # добавляем юзера, который создает беседу
    def validate(self, attrs):
        # print(2)
        try:
            attrs['user']
        except KeyError:
            raise exceptions.ValidationError('Поле user обязательно')

        if not attrs['user']:
            attrs['user'].append(self.context['user'].id)
        return attrs

    class Meta:
        model = Chat
        fields = ['id', 'name', 'message', 'user']
        extra_kwargs = {
            'user': {'required': True}, }


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
