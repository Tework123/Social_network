from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from login.models import ProfilePhoto
from login.serializers import ProfileSerializer, CreateUserSerializer, AuthUserSerializer, ProfilePhotoSerializer
from django.contrib.auth import authenticate, login, logout

from login.utils import account_activation_token


class ProfileList(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)

        mail_subject = 'Ссылка для активации аккаунта'
        user = self.request.user
        message = render_to_string('email_auth.html', {
            'user': user,

            # нужно сделать domain меняющимся, сервер или локальная машина
            # в темплайте надо будет еще изменить http на https
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = request.data['email']
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

        return Response({
            'status': 200,
            'message': 'Для подтверждения аккаунта пройди по ссылке,'
                       ' которая отправлена вам на почту',
        })


# надо получить с фронта емайл
@api_view(('POST',))
def send_token_to_email(request):
    mail_subject = 'Ссылка для активации аккаунта'
    user = request.user
    message = render_to_string('email_auth.html', {
        'user': user,

        # нужно сделать domain меняющимся, сервер или локальная машина
        # в темплайте надо будет еще изменить http на https
        'domain': '127.0.0.1:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = request.data['email']
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()


@api_view(('GET',))
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        # return redirect('home')
        return Response('Ваш аккаунт активирован')
    else:
        return Response('Время жизни ссылки истекло')


class AuthUserView(CreateAPIView):
    serializer_class = AuthUserSerializer

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=request.data['email'])

        user = authenticate(username=user.username, password=request.data['password'])
        print(user)
        if user is not None:
            login(request, user)

        # print(user.is_active)
        return Response({
            'status': 200,
            'message': 'Авторизация прошла успешно',
        })


class LogoutUserView(APIView):

    def get(self, request):
        logout(request)
        return Response('Выход из аккаунта выполнен успешно')


class ProfilePhotoTest(ListAPIView, CreateAPIView):
    queryset = ProfilePhoto.objects.all()
    serializer_class = ProfilePhotoSerializer
