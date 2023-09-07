from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from login.email import send_to_email
from login.models import CustomUser
from login.serializers import ProfileSerializer, CreateUserSerializer, AuthUserSerializer, \
    ResetPasswordSendEmailSerializer, ResetPasswordCreatePasswordSerializer
from django.contrib.auth import authenticate, login, logout

from login.utils import account_activation_token


class GetProfile(ListAPIView):
    pass
