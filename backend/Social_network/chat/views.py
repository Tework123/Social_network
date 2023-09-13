import datetime

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status, viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from album.models import Photo
from chat.models import Chat, Relationship, Message
from chat.serializers import ChatListSerializer, ChatEditSerializer, RelationshipListSerializer, \
    RelationshipEditSerializer, MessageChatListSerializer, MessageChatCreateSerializer, MessageChatEditSerializer, \
    MessageMockChatSerializer


class ChatListView(generics.ListCreateAPIView):
    """Показывает все чаты пользователя, создает чат"""
    serializer_class = ChatListSerializer

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        chat = Chat.objects.create(name=request.data['name'], open_or_close=True)

        # добавлять не любых юзеров можно в чат, а только друзей, как отсортировать
        # в дополнениях к запросу отправить список юзеров?
        # на фронте все равно не будет списка, как здесь в rest
        for user in request.data.getlist('user'):
            chat.user.add(user)

        return Response(status=status.HTTP_201_CREATED, data='Беседа создана успешно')


class ChatEditView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает один чат, изменяет, удаляет его(требуется id чата)"""
    serializer_class = ChatEditSerializer

    def get_object(self):
        return get_object_or_404(Chat, pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        chat = Chat.objects.filter(pk=self.kwargs['pk'])

        chat.update(name=request.data['name'])

        # удаляем все прикрепленные many_to_many objects
        chat[0].user.clear()

        for user in request.data.getlist('user'):
            chat[0].user.add(user)

        return Response(status=status.HTTP_200_OK, data='Беседа успешно изменена')

    def delete(self, request, *args, **kwargs):
        Chat.objects.get(pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_200_OK, data='Беседа успешно удалена')


class RelationshipListView(generics.ListCreateAPIView):
    """Показывает все диалоги, создает диалог"""

    serializer_class = RelationshipListSerializer

    def get_queryset(self):
        user = self.request.user
        return Relationship.objects.filter(Q(user_1=user) | Q(user_2=user))

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_2 = request.data['user_2']
        exist_relationship = Relationship.objects.filter(Q(user_1=user, user_2=user_2) |
                                                         Q(user_2=user, user_1=user_2))

        if exist_relationship:
            return Response(status=status.HTTP_200_OK, data='Этот пользователь уже связан с тобой')

        Relationship.objects.create(user_1=user,
                                    user_2_id=user_2,
                                    status=request.data['status'])

        return Response(status=status.HTTP_201_CREATED, data='Отношения с пользователем установлены')


class RelationshipEditView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает один диалог, изменяет, удаляет его(требуется id диалога)"""

    serializer_class = RelationshipEditSerializer

    def get_object(self):
        return get_object_or_404(Relationship, pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        relationship = Relationship.objects.filter(pk=self.kwargs['pk'])
        relationship.update(status=request.data['status'])
        return Response(status=status.HTTP_200_OK, data='Отношения с пользователем изменены')

    # что такое черный список? Это отношения, но если удалить из друзей, то отношений нет
    # при этом в черном списке человек должен оставаться
    def delete(self, request, *args, **kwargs):
        Relationship.objects.get(pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_200_OK, data='Отношения успешно удалены')


#  permissions
#  когда пытается получить доступ к чату из url, то будет блок, ничего не показывает, просто блокирует
# когда ты не состоишь в этом чате, можно только по приглашению? Либо специальная кнопка для
# вступления в чат(в группах например)

class MessageChatListView(viewsets.ModelViewSet):
    """Показывает все сообщения одного чата, отправляет созданное сообщение(требуется id чата)"""

    serializer_classes = {'list': MessageChatListSerializer,
                          'put': MessageChatCreateSerializer}
    default_serializer_class = MessageChatListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return Message.objects.filter(chat__pk=self.kwargs['pk'], mock=False).order_by('-date_create')

    # здесь нужен put для обновления поля mock = False
    def put(self, request, *args, **kwargs):
        message = Message.objects.filter(user=self.request.user, chat_id=self.kwargs['pk'], mock=True)
        message.update(mock=False, text=request.data['text'], date_create=timezone.now())

        return Response(status=status.HTTP_201_CREATED, data='Сообщение добавлено в чат')


class MessageCreateMockChatView(generics.RetrieveUpdateDestroyAPIView):
    """(GET) Показывает mock=True(черновик) сообщение этого чата,
     создает сообщение(mock=True, черновик)(требуется id чата)
     (PUT) Добавляет фото из альбома к сообщению"""

    serializer_class = MessageMockChatSerializer

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
        mock_message = Message.objects.get(user=self.request.user,
                                           chat_id=self.kwargs['pk'], mock=True)

        mock_message.photo.clear()
        photos = request.data.getlist('photo')
        for photo in photos:
            mock_message.photo.add(photo)

        return Response(status=status.HTTP_200_OK, data='Фото добавлены к сообщению')


class MessageChatEditView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает, изменяет, удаляет одно сообщение(требуется id сообщения)"""
    serializer_class = MessageChatEditSerializer

    def get_object(self):
        # достать еще все фото с новым сериализатором
        return get_object_or_404(Message.objects.prefetch_related('photo'), pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        message = Message.objects.filter(pk=self.kwargs['pk'])

        message[0].photo.clear()
        photos = request.data.getlist('photo')
        for photo in photos:
            message[0].photo.add(photo)

        message.update(text=request.data['text'], date_change=timezone.now())
        return Response(status=status.HTTP_200_OK, data='Сообщение изменено')

    def delete(self, request, *args, **kwargs):
        Message.objects.get(pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_200_OK, data='Сообщение удалено')

# протестировать все вручную

# далее надо диалоги сделать, посмотреть как будет работать прикрепление фоточек,
# потом уже permissions,
