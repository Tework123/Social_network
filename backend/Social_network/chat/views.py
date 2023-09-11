from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from chat.models import Chat
from chat.serializers import ChatListSerializer, ChatEditSerializer


# создать чат
# изменить чата, удалить чат
# добавить друга в чат, удалить друга из чата
# добавить друга(создает relationship, тоже что и чат
# создать сообщение в чат или другу
# удалить сообщение, редактировать сообщение
class ChatListView(generics.ListCreateAPIView):
    """Показывает все чаты пользователя, создает чат"""
    serializer_class = ChatListSerializer

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        chat = Chat.objects.create(name=request.data['name'], open_or_close=True)

        for user in request.data.getlist('user'):
            chat.user.add(user)

        return Response(status=status.HTTP_201_CREATED, data='Беседа создана успешно')


# добавить друзей в чат, сразу несколько как
class ChatEditView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает один чат, изменяет, удаляет его"""
    serializer_class = ChatEditSerializer

    def get_object(self):
        return get_object_or_404(Chat, pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, pk=self.kwargs['pk'])

        for user in request.data.getlist('user'):
            chat.user.add(user)
        return Response(status=status.HTTP_200_OK, data='Беседа успешно изменена')

    def delete(self, request, *args, **kwargs):
        Chat.objects.get(pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_200_OK, data='Беседа успешно удалена')


class RelationshipListView():
    pass
    # оттестировать предыдущий класс
    # переписываем с прошлого проекта, аккуратно, используем новые знания.


class MessageListView():
    pass
