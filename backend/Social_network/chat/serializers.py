from rest_framework import serializers, exceptions
from chat.models import Chat, Relationship, Message


# chat
class ChatListSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField('last_message')

    # Чтобы показать последнее сообщения каждого чата, нужно делать дополнительный запрос
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
        extra_kwargs = {
            'id': {'required': True},
            'text': {'required': True}, }


class MessageChatEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'photo']
        extra_kwargs = {
            'id': {'required': True},
            'text': {'required': True},
            'photo': {'required': True},
        }


class MessageMockChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'photo']
        extra_kwargs = {
            'id': {'required': True},
            'photo': {'required': True}, }


# dialogs
class RelationshipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id', 'user_1', 'user_2', 'status']


class RelationshipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['user_2', 'status']
        extra_kwargs = {
            'user_2': {'required': True},
            'status': {'required': True}, }


class RelationshipEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True}, }
