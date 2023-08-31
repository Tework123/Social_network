from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import ListAPIView

from login.serializers import ProfileSerializer


class ProfileList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    print(1)