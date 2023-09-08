import rest_framework
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import AccountSerializer
from login.email import send_to_email
from account.models import CustomUser
from login.serializers import ProfileSerializer, CreateUserSerializer, AuthUserSerializer, \
    ResetPasswordSendEmailSerializer, ResetPasswordCreatePasswordSerializer
from django.contrib.auth import authenticate, login, logout

from login.utils import account_activation_token


class AccountView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer

    # lookup_field = 'pk'
    # надо посмотреть что в таблице контент тайп по гайдам
    def get_queryset(self):
        # return get_object_or_404(CustomUser, email=self.request.user)
        print(self.kwargs['pk'])

        return CustomUser.objects.filter(pk=self.kwargs['pk']).select_related('content_type').prefetch_related('education')

    def update(self, request, *args, **kwargs):
        pass

# страница профиля

# get_account получить всю инфу аккаунта, в том числе группы, друзей,
# подгрузить три последние фото из моих альбомов

# change_account изменить любое поле в аккаунте

# получить

# получить все посты, которые к моей странице привязаны
