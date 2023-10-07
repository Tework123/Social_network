from rest_framework import serializers
from chat.models import Chat, Relationship, Message


# chat
class ChatListGETSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField('last_message')

    # Чтобы показать последнее сообщения каждого чата, нужно делать дополнительный запрос
    def last_message(self, obj):
        last_message = Message.objects.filter(chat_id=obj.pk).prefetch_related(
            'photo').order_by('-date_create')[:1]
        return MessageRetrieveSerializer(last_message, many=True).data

    class Meta:
        model = Chat
        fields = ['id',
                  'name',
                  'message',
                  'user']


class ChatPOSTSerializer(serializers.ModelSerializer):

    # добавляем юзера, который создает беседу
    def validate(self, attrs):
        attrs['user'].append(self.context['user'].id)
        return attrs

    class Meta:
        model = Chat
        fields = ['name',
                  'user']
        extra_kwargs = {
            'user': {'required': True}, }


class ChatRetrieveGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id',
                  'name',
                  'user']


class ChatRetrievePATCHSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['name',
                  'user']


# chat message
class MessageChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id',
                  'text',
                  'date_create',
                  'date_change',
                  'user',
                  'mock',
                  'photo']


class MessageChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id',
                  'text']
        extra_kwargs = {
            'id': {'required': True},
            'text': {'required': True}, }


class MessageMockChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id',
                  'photo']
        extra_kwargs = {
            'id': {'required': True},
            'photo': {'required': True}, }


class MessageRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id',
                  'text',
                  'photo']


# dialogs
class RelationshipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id',
                  'user_1',
                  'user_2',
                  'status']


class RelationshipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['user_2',
                  'status']


class RelationshipRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['status']
