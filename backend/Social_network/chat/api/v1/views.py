from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import Chat, Relationship, Message
from chat.api.permissions import IsChatUser, IsMessageCreator, IsRelationshipUser
from chat.api.serializers import (
    RelationshipListSerializer,
    MessageChatListSerializer,
    MessageChatCreateSerializer,
    MessageMockChatSerializer, RelationshipCreateSerializer, ChatListGETSerializer,
    ChatPOSTSerializer, ChatRetrievePATCHSerializer, ChatRetrieveGETSerializer,
    MessageRetrieveSerializer, RelationshipRetrieveSerializer)


class ChatListView(generics.ListCreateAPIView):
    """Показывает все чаты пользователя с первым сообщением каждого чата, создает чат"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChatListGETSerializer
        else:
            return ChatPOSTSerializer

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).prefetch_related('user')

    def post(self, request, *args, **kwargs):

        # чтобы создатель автоматически добавлялся в чат
        serializer = ChatPOSTSerializer(data=request.data, context={'user': self.request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data='Беседа создана успешно')


class ChatRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает один чат, изменяет, удаляет его(требуется id чата)"""
    permission_classes = [IsAuthenticated, IsChatUser]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChatRetrieveGETSerializer
        else:
            return ChatRetrievePATCHSerializer

    def get_object(self):
        return get_object_or_404(Chat.objects.prefetch_related('user'), pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Беседа успешно изменена')

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Беседа успешно удалена')


class MessageChatListView(viewsets.ModelViewSet):
    """Показывает все сообщения одного чата, отправляет созданное сообщение(требуется id чата)"""

    serializer_classes = {'list': MessageChatListSerializer,
                          'put': MessageChatCreateSerializer}
    default_serializer_class = MessageChatListSerializer
    permission_classes = [IsAuthenticated, IsChatUser]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return (Message.objects.filter(chat__pk=self.kwargs['pk'], mock=False)
                .prefetch_related('photo').order_by('-date_create'))

    # здесь нужен put для обновления поля mock = False
    def put(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)

        serializer = MessageChatCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = Message.objects.filter(user=self.request.user,
                                         chat_id=self.kwargs['pk'], mock=True)
        message.update(mock=False, text=request.data['text'], date_create=timezone.now())

        return Response(status=status.HTTP_201_CREATED, data='Сообщение добавлено в чат')


class MessageCreateMockChatView(generics.RetrieveUpdateDestroyAPIView):
    """(GET) Показывает mock=True(черновик) сообщение этого чата,
     создает сообщение(mock=True, черновик)(требуется id чата)
     (PUT) Добавляет фото из альбома к сообщению"""

    serializer_class = MessageMockChatSerializer
    permission_classes = [IsAuthenticated, IsChatUser]

    def get_object(self):
        chat = get_object_or_404(Chat, pk=self.kwargs['pk'])
        try:
            mock_message = Message.objects.get(user=self.request.user, chat__pk=chat.pk,
                                               mock=True)
        except:
            mock_message = Message.objects.create(text='',
                                                  user=self.request.user,
                                                  chat_id=chat.pk,
                                                  mock=True)
        return mock_message

    def put(self, request, *args, **kwargs):
        serializer = MessageMockChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mock_message = Message.objects.get(user=self.request.user,
                                           chat_id=self.kwargs['pk'], mock=True)

        mock_message.photo.clear()

        # здесь нужны id уже сохраненных на сервере photo
        photos = request.data['photo']
        for photo in photos:
            mock_message.photo.add(photo)

        return Response(status=status.HTTP_200_OK, data='Фото добавлены к сообщению')


# Relationship
class RelationshipListView(generics.ListCreateAPIView):
    """Показывает все отношения, создает отношения"""

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RelationshipListSerializer
        else:
            return RelationshipCreateSerializer

    def get_queryset(self):
        user = self.request.user
        return Relationship.objects.filter(Q(user_1=user) | Q(user_2=user))

    # создать отношение - начать переписку с любым пользователем
    # кстати, отношения с самим собой (избранное в VK, надо автоматически создавать)
    def post(self, request, *args, **kwargs):
        serializer = RelationshipCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        user_2 = request.data['user_2']
        exist_relationship = Relationship.objects.filter(Q(user_1=user, user_2=user_2)
                                                         | Q(user_2=user, user_1=user_2))

        if exist_relationship:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data='Этот пользователь уже связан с тобой')

        serializer.save(user_1=user)

        return Response(status=status.HTTP_201_CREATED,
                        data='Отношения с пользователем установлены')


class RelationshipRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает один диалог, изменяет, удаляет его(требуется id диалога)"""

    serializer_class = RelationshipRetrieveSerializer
    permission_classes = [IsAuthenticated, IsRelationshipUser]

    def get_object(self):
        return get_object_or_404(Relationship.objects.
                                 select_related('user_1', 'user_2'), pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Отношения с пользователем изменены')

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Отношения успешно удалены')


class MessageRelationshipListView(viewsets.ModelViewSet):
    """Показывает все сообщения одного отношения,
     отправляет созданное сообщение(требуется id отношения)"""

    serializer_classes = {'list': MessageChatListSerializer,
                          'put': MessageChatCreateSerializer}
    default_serializer_class = MessageChatListSerializer
    permission_classes = [IsAuthenticated, IsRelationshipUser]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return (Message.objects.filter(relationship__pk=self.kwargs['pk'], mock=False)
                .prefetch_related('photo').order_by('-date_create'))

    def put(self, request, *args, **kwargs):
        serializer = MessageChatCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = Message.objects.filter(user=self.request.user,
                                         relationship_id=self.kwargs['pk'], mock=True)
        message.update(mock=False, text=request.data['text'], date_create=timezone.now())

        return Response(status=status.HTTP_201_CREATED,
                        data='Сообщение добавлено в отношение')


class MessageCreateMockRelationshipView(generics.RetrieveUpdateDestroyAPIView):
    """(GET) Показывает mock=True(черновик) сообщение этого диалога,
     создает сообщение(mock=True, черновик)(требуется id диалога)
     (PUT) Добавляет фото из альбома к сообщению"""

    serializer_class = MessageMockChatSerializer
    permission_classes = [IsAuthenticated, IsRelationshipUser]

    def get_object(self):
        relationship = get_object_or_404(Relationship, pk=self.kwargs['pk'])
        try:
            mock_message = Message.objects.get(user=self.request.user,
                                               relationship__pk=relationship.pk,
                                               mock=True)
        except:
            mock_message = Message.objects.create(text='',
                                                  user=self.request.user,
                                                  relationship_id=relationship.pk,
                                                  mock=True)
        return mock_message

    def put(self, request, *args, **kwargs):
        serializer = MessageMockChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mock_message = Message.objects.get(user=self.request.user,
                                           relationship_id=self.kwargs['pk'], mock=True)

        mock_message.photo.clear()

        photos = request.data['photo']
        for photo in photos:
            mock_message.photo.add(photo)

        return Response(status=status.HTTP_200_OK, data='Фото добавлены к сообщению')


class MessageRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает, изменяет, удаляет одно сообщение(требуется id сообщения)"""
    permission_classes = [IsAuthenticated, IsMessageCreator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MessageChatListSerializer
        else:
            return MessageRetrieveSerializer

    def get_object(self):
        return get_object_or_404(Message.objects.prefetch_related('photo'),
                                 pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        serializer.save(date_change=timezone.now())

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Сообщение изменено')

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Сообщение удалено')
