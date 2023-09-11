from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from login.email import send_to_email
from account.models import CustomUser
from login.serializers import CreateUserSerializer, AuthUserSerializer, \
    ResetPasswordSendEmailSerializer, ResetPasswordCreatePasswordSerializer
from django.contrib.auth import authenticate, login, logout

from login.utils import account_activation_token

response_schema_dict = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "200_key1": "200_value_1",
                "200_key2": "200_value_2",
            }
        }
    ),
    "205": openapi.Response(
        description="custom 205 description",
        examples={
            "application/json": {
                "205_key1": "205_value_1",
                "205_key2": "205_value_2",
            }
        }
    ),
}


class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer

    @swagger_auto_schema(responses=response_schema_dict)
    # @swagger_auto_schema(operation_description="partial_update description override", responses={404: 'slug not found'})
    # @swagger_auto_schema(method='post', operation_description="HELLO EVERYONE")
    @action(detail=False, methods=['post'])
    def post(self, request, *args, **kwargs):
        try:
            CustomUser.objects.get(email=self.request.data['email'])
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Этот email уже занят')
        except Exception:

            user = CustomUser.objects.create_user(email=self.request.data['email'],
                                                  password=self.request.data['password'],
                                                  is_active=False)

            # отправка на email
            send_to_email(user, mail_subject='Ссылка для активации аккаунта',
                          template_name='email_auth.html')

            return Response(status=status.HTTP_200_OK,
                            data='Для подтверждения аккаунта пройди по ссылке,'
                                 ' которая отправлена вам на почту')


class RegisterUserTryView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, email=request.data['email'])
        if user.is_active:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Ваш аккаунт уже подтвержден')

        # отправка на email
        send_to_email(user, mail_subject='Ссылка для активации аккаунта',
                      template_name='email_auth.html')

        return Response(status=status.HTTP_200_OK,
                        data='Для подтверждения аккаунта пройди по ссылке,'
                             ' которая отправлена вам на почту')


class AuthUserView(CreateAPIView):
    serializer_class = AuthUserSerializer

    def post(self, request, *args, **kwargs):
        if request.data['email'] == 'user@mail.ru' and request.data['password'] == 'user@mail.ru':
            try:
                user = CustomUser.objects.get(email=request.data['email'])
            except Exception:
                user = CustomUser.objects.create_user(email=self.request.data['email'],
                                                      password=self.request.data['password'],
                                                      is_active=True)

            user = authenticate(email=user.email, password=request.data['password'])
            login(request, user)

            return Response(status=status.HTTP_200_OK,
                            data='Авторизация тестового юзера прошла успешно')

        user = get_object_or_404(CustomUser, email=request.data['email'])

        user = authenticate(email=user.email, password=request.data['password'])
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

        # return redirect('home')
        return Response(status=status.HTTP_200_OK, data='Ваш аккаунт активирован')
    else:
        return Response(status=status.HTTP_403_FORBIDDEN, data='Время жизни ссылки истекло')


class ResetPasswordSendEmail(CreateAPIView):
    serializer_class = ResetPasswordSendEmailSerializer

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, email=request.data['email'])

        # отправка на email
        send_to_email(user, mail_subject='Ссылка для сброса пароля',
                      template_name='email_reset_password.html')

        return Response(status=status.HTTP_200_OK,
                        data='Для сброса пароля пройдите по ссылке,'
                             ' которая отправлена вам на почту')


class ResetPasswordCreatePassword(APIView):

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
        # print(self.request.data['confirm_password'])

        # if self.request.data['password'] != self.request.data['confirm_password']:
        #     return Response({
        #         'status': 400,
        #         'message': 'Введенные пароли не совпадают',
        #     })

        user.set_password(serializer.data['password'])
        user.save()

        return Response(status=status.HTTP_200_OK, data='Пароль изменен успешно')


class LogoutUserView(APIView):

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK, data='Выход из аккаунта выполнен успешно')


class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_200_OK, data='Аккаунт удален успешно')
