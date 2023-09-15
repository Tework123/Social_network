import datetime

from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, status, viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from album.models import Photo
from chat.models import Chat, Relationship, Message
from chat.permissions import IsChatUser, IsChatUserDetail
from chat.serializers import ChatListSerializer, ChatEditSerializer, RelationshipListSerializer, \
    RelationshipEditSerializer, MessageChatListSerializer, MessageChatCreateSerializer, MessageChatEditSerializer, \
    MessageMockChatSerializer, RelationshipCreateSerializer


class ChatListView(generics.ListCreateAPIView):
    """Показывает все чаты пользователя, создает чат"""
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        chat = Chat.objects.create(name=request.data['name'], open_or_close=True)

        # в дополнениях к запросу отправить список юзеров? Просто запрос будет на relationship
        # нужна отдельная урл на запрос друзей получается, where status = friend
        # на фронте помечаешь нужных, отправляешь post запрос сюда
        # на фронте все равно не будет списка, как здесь в rest
        for user in request.data.getlist('user'):
            chat.user.add(user)

        return Response(status=status.HTTP_201_CREATED, data='Беседа создана успешно')


class ChatEditView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает один чат, изменяет, удаляет его(требуется id чата)"""
    serializer_class = ChatEditSerializer
    permission_classes = [IsAuthenticated, IsChatUser]

    def get_object(self):
        return get_object_or_404(Chat.objects.prefetch_related('user'), pk=self.kwargs['pk'])

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
        message = Message.objects.filter(user=self.request.user, chat_id=self.kwargs['pk'], mock=True)
        message.update(mock=False, text=request.data['text'], date_create=timezone.now())

        return Response(status=status.HTTP_201_CREATED, data='Сообщение добавлено в чат')


class MessageCreateMockChatView(generics.RetrieveUpdateDestroyAPIView):
    """(GET) Показывает mock=True(черновик) сообщение этого чата,
     создает сообщение(mock=True, черновик)(требуется id чата)
     (PUT) Добавляет фото из альбома к сообщению"""

    serializer_class = MessageMockChatSerializer
    # здесь не нужен отдельный permissions, доступ по pk только к чату
    permission_classes = [IsAuthenticated]

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
    permission_classes = []

    #

    def get_object(self):
        # достать еще все фото с новым сериализатором
        return get_object_or_404(Message.objects.prefetch_related('photo'), pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        message = Message.objects.filter(pk=self.kwargs['pk'])

        # Когда фронт возвращает выбранные фото пользователем, тогда приходит словарь,
        # а не QueryDict django(из граф. интерфейса), поэтому нужны преобразования: уже без getlist
        if type(request.data) == dict:
            query_dict = QueryDict('', mutable=True)
            query_dict.update(request.data)
            photos = query_dict['photo']
        else:
            photos = request.data.getlist('photo')

        message[0].photo.clear()
        for photo in photos:
            message[0].photo.add(photo)

        message.update(text=request.data['text'], date_change=timezone.now())
        return Response(status=status.HTTP_200_OK, data='Сообщение изменено')

    def delete(self, request, *args, **kwargs):
        Message.objects.get(pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_200_OK, data='Сообщение удалено')


# Relationship
class RelationshipListView(viewsets.ModelViewSet):
    """Показывает все отношения, создает отношения"""

    serializer_classes = {'list': RelationshipListSerializer,
                          'post': RelationshipCreateSerializer}
    default_serializer_class = RelationshipListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        user = self.request.user
        return Relationship.objects.filter(Q(user_1=user) | Q(user_2=user))

    # создать отношение - начать переписку с любым пользователем
    def post(self, request, *args, **kwargs):
        user = self.request.user

        # нужна будет кнопка для создания отношения в профиле каждого человека,
        # с которым еще нет диалога, там уже подхватывается его id
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
    # это будет особое отношение, в друзьях показываться не будет, писать не сможет
    def delete(self, request, *args, **kwargs):
        Relationship.objects.get(pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_200_OK, data='Отношения успешно удалены')


#  permissions
#  когда пытается получить доступ к чату из url, то будет блок, ничего не показывает, просто блокирует
# когда ты не состоишь в этом чате, можно только по приглашению? Либо специальная кнопка для
# вступления в чат(в группах например)
class MessageRelationshipListView(viewsets.ModelViewSet):
    """Показывает все сообщения одного диалога, отправляет созданное сообщение(требуется id диалога)"""

    serializer_classes = {'list': MessageChatListSerializer,
                          'put': MessageChatCreateSerializer}
    default_serializer_class = MessageChatListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return Message.objects.filter(relationship__pk=self.kwargs['pk'], mock=False).order_by('-date_create')

    # здесь нужен put для обновления поля mock = False
    def put(self, request, *args, **kwargs):
        message = Message.objects.filter(user=self.request.user, relationship_id=self.kwargs['pk'], mock=True)
        message.update(mock=False, text=request.data['text'], date_create=timezone.now())

        return Response(status=status.HTTP_201_CREATED, data='Сообщение добавлено в отношение')


class MessageCreateMockRelationshipView(generics.RetrieveUpdateDestroyAPIView):
    """(GET) Показывает mock=True(черновик) сообщение этого диалога,
     создает сообщение(mock=True, черновик)(требуется id диалога)
     (PUT) Добавляет фото из альбома к сообщению"""

    serializer_class = MessageMockChatSerializer

    def get_object(self):
        relationship = get_object_or_404(Relationship, pk=self.kwargs['pk'])
        try:
            mock_message = Message.objects.get(user=self.request.user, relationship__pk=relationship.pk,
                                               mock=True)
        except:
            mock_message = Message.objects.create(text='',
                                                  user=self.request.user,
                                                  relationship_id=relationship.pk,
                                                  mock=True)
        return mock_message

    def put(self, request, *args, **kwargs):
        mock_message = Message.objects.get(user=self.request.user,
                                           relationship_id=self.kwargs['pk'], mock=True)

        mock_message.photo.clear()
        photos = request.data.getlist('photo')
        for photo in photos:
            mock_message.photo.add(photo)

        return Response(status=status.HTTP_200_OK, data='Фото добавлены к сообщению')

# потом уже permissions,
