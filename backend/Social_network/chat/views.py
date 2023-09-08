from django.shortcuts import render
from rest_framework import generics

from chat.models import Chat
from chat.serializers import ChatListSerializer


class GetChats(generics.ListAPIView):
    serializer_class = ChatListSerializer
    queryset = Chat.objects.all()
