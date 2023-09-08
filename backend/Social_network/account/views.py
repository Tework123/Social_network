import rest_framework
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import AccountSerializer, AccountEditSerializer
from login.email import send_to_email
from account.models import CustomUser
from login.serializers import ProfileSerializer, CreateUserSerializer, AuthUserSerializer, \
    ResetPasswordSendEmailSerializer, ResetPasswordCreatePasswordSerializer
from django.contrib.auth import authenticate, login, logout

from login.utils import account_activation_token


class AccountView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.kwargs['pk']).prefetch_related('education', 'work', 'groups')
        # select_related('content_type')


# надо попробовать написать свою вьюапи и сериализатор и вытащить все про пользователя
# также его друзей(relationships), группы(communa), еще посты.
class AccountEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountEditSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.kwargs['pk']).prefetch_related('education', 'work', 'groups')

    def update(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(pk=self.kwargs['pk'])

        user.update(first_name=request.data['first_name'],
                    last_name=request.data['last_name'], phone=request.data['phone'],
                    city=request.data['city'], about_me=request.data['about_me'],
                    avatar=request.data['avatar'], date_of_birth=request.data['date_of_birth'],
                    lifestyle=request.data['lifestyle'], interest=request.data['interest'])
        return Response(status=status.HTTP_200_OK, data='Информация успешно изменена')


