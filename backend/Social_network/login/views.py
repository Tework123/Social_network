from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from login.utils import send_email_env
from account.models import CustomUser
from login.serializers import (ResetPasswordCreatePasswordSerializer,
                               RegisterSerializer, RegisterTrySerializer,
                               AuthSerializer)
from django.contrib.auth import authenticate, login, logout

from login.email import account_activation_token
from login.utils import create_test_user


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            CustomUser.objects.get(email=request.data['email'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Этот email уже занят')
        except:

            user = serializer.save()

            send_email_env(email=user.email,
                           mail_subject='Ссылка для активации аккаунта',
                           template_name='email_auth.html')

            return Response(status=status.HTTP_200_OK,
                            data='Для подтверждения аккаунта пройди по ссылке,'
                                 ' которая отправлена вам на почту')


class RegisterTryView(CreateAPIView):
    serializer_class = RegisterTrySerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterTrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(CustomUser, email=request.data['email'])
        if user.is_active:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Ваш аккаунт уже подтвержден')

        send_email_env(email=user.email,
                       mail_subject='Ссылка для активации аккаунта',
                       template_name='email_auth.html')

        return Response(status=status.HTTP_200_OK,
                        data='Для подтверждения аккаунта пройди по ссылке,'
                             ' которая отправлена вам на почту')


class AuthView(CreateAPIView):
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data['email']
        password = request.data['password']

        if email == 'user@mail.ru' and password == 'user@mail.ru':
            create_test_user(email, password, request)

            return Response(status=status.HTTP_200_OK,
                            data='Авторизация тестового юзера прошла успешно')

        user = get_object_or_404(CustomUser, email=email)

        user = authenticate(email=user.email, password=password)

        if user is None:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data='Данные для авторизации неправильные')

        login(request, user)

        return Response(status=status.HTTP_200_OK, data='Вход выполнен успешно')


@api_view(('GET',))
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(CustomUser, pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True
        user.save()
        login(request, user)
        return Response(status=status.HTTP_200_OK, data='Ваш аккаунт активирован')
    else:
        return Response(status=status.HTTP_403_FORBIDDEN, data='Время жизни ссылки истекло')


class ResetPasswordSendEmailView(CreateAPIView):
    serializer_class = RegisterTrySerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterTrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(CustomUser, email=request.data['email'])

        send_email_env(email=user.email,
                       mail_subject='Ссылка для сброса пароля',
                       template_name='email_reset_password.html')

        return Response(status=status.HTTP_200_OK,
                        data='Для сброса пароля пройдите по ссылке,'
                             ' которая отправлена вам на почту')


class ResetPasswordCreatePasswordView(APIView):

    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return Response(status=status.HTTP_200_OK, data='Введите новый пароль')

    def post(self, request, uidb64, token):
        serializer = ResetPasswordCreatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is None and not account_activation_token.check_token(user, token):
            return Response(status=status.HTTP_403_FORBIDDEN, data='Время жизни ссылки истекло')

        user = get_object_or_404(CustomUser, email=user.email)
        user.set_password(serializer.data['password'])
        user.save()

        return Response(status=status.HTTP_200_OK, data='Пароль изменен успешно')


class LogoutUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK, data='Выход из аккаунта выполнен успешно')


class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_200_OK, data='Аккаунт удален успешно')
