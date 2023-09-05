from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from login.email import send_to_email
from login.models import ProfilePhoto, CustomUser
from login.serializers import ProfileSerializer, CreateUserSerializer, AuthUserSerializer, ProfilePhotoSerializer, \
    ResetPasswordSendEmailSerializer, ResetPasswordCreatePasswordSerializer
from django.contrib.auth import authenticate, login, logout

from login.utils import account_activation_token


class ProfileList(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer


class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(email=self.request.data['email'])
        if user:
            return Response({
                'status': 200,
                'message': 'Этот email уже занят',
            })

        user = CustomUser.objects.create_user(email=self.request.data['email'],
                                              password=self.request.data['password'],
                                              is_active=False)

        # отправка на email
        send_to_email(user, mail_subject='Ссылка для активации аккаунта',
                      template_name='email_auth.html')

        return Response({
            'status': 200,
            'message': 'Для подтверждения аккаунта пройди по ссылке,'
                       ' которая отправлена вам на почту',
        })


class AuthUserView(CreateAPIView):
    serializer_class = AuthUserSerializer

    def post(self, request, *args, **kwargs):
        if request.data['email'] == 'user@mail.ru' and request.data['password'] == 'user@mail.ru':
            user = CustomUser.objects.filter(email=request.data['email'])

            if not user:
                user = CustomUser.objects.create_user(email=self.request.data['email'],
                                                      password=self.request.data['password'],
                                                      is_active=True)

            user = authenticate(email=user[0].email, password=request.data['password'])
            login(request, user)
            return Response({
                'status': 200,
                'message': 'Вход тестового пользователя выполнен успешно',
            })

        user = get_object_or_404(CustomUser, email=request.data['email'])

        user = authenticate(email=user.email, password=request.data['password'])
        if user is None:
            return Response({
                'status': 403,
                'message': 'Данные для авторизации неправильные',
            })

        login(request, user)

        return Response({
            'status': 200,
            'message': 'Авторизация прошла успешно',
        })


class LogoutUserView(APIView):

    def get(self, request):
        logout(request)
        return Response('Выход из аккаунта выполнен успешно')


class ResetPasswordSendEmail(CreateAPIView):
    serializer_class = ResetPasswordSendEmailSerializer

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, email=request.data['email'])

        # отправка на email
        send_to_email(user, mail_subject='Ссылка для сброса пароля',
                      template_name='email_reset_password.html')

        return Response({
            'status': 200,
            'message': 'Для сброса пароля пройдите по ссылке,'
                       ' которая отправлена вам на почту',
        })


class ResetPasswordCreatePassword(APIView):
    serializer_class = ResetPasswordCreatePasswordSerializer

    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return Response({
                'status': 200,
                'message': 'Введите новый пароль',
            })

    def post(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError):
            user = None

        if user is None and not account_activation_token.check_token(user, token):
            return Response()
        user = get_object_or_404(CustomUser, email=user.email)
        print(self.request.data['confirm_password'])

        if self.request.data['password'] != self.request.data['confirm_password']:
            return Response({
                'status': 400,
                'message': 'Введенные пароли не совпадают',
            })
        user.set_password(self.request.data['password'])
        user.save()

        return Response({
            'status': 200,
            'message': 'Ваш пароль изменен успешно'
        })


# @api_view(('GET',))
# def reset_password(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = CustomUser.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         return Response({
#             'status': 200,
#             'message': 'Введите новый пароль',
#         })
#     else:
#         return Response({
#             'status': 200,
#             'message': 'Возникла проблема',
#         })


@api_view(('GET',))
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        # return redirect('home')
        return Response('Ваш аккаунт активирован')
    else:
        return Response('Время жизни ссылки истекло')


class ProfilePhotoTest(ListAPIView, CreateAPIView):
    queryset = ProfilePhoto.objects.all()
    serializer_class = ProfilePhotoSerializer
