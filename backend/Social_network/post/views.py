import json
import time

from celery.result import AsyncResult
from django.db import transaction
from django.http import HttpResponse
from rest_framework import generics, status, views
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tasks.tasks import task_db

from post.models import Post
from post.serializers import PostListSerializer, PostCreateSerializer

import logging

log = logging.getLogger(__name__)


class CreatePostView(generics.ListCreateAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        else:
            return PostCreateSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).prefetch_related('photo')

    def post(self, request, *args, **kwargs):
        # сделать с celery
        serializer = PostCreateSerializer(data=request.data, context={'user': self.request.user})
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                # save instance
                instance = serializer.save()
                instance.save()

                # create task params
                job_params = {"id": instance.id}

                # submit task for background execution
                task = transaction.on_commit(lambda: task_db.delay(job_params))

        except Exception as e:
            raise APIException(str(e))
        # serializer.save()

        return Response(status=status.HTTP_201_CREATED, data=f'Пост успешно создан,'
                                                             f'res={task.status}')


class PostEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostCreateSerializer

    def get_queryset(self):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        posts = Post.objects.all().delete()
        # for i in posts:
        #     Post.objects.get(pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_200_OK, data='Пост успешно удален')


import requests


class DigitalAPiView(views.APIView):

    def get(self, request):
        # url = 'https://api.dictionaryapi.dev/api/v2/entries/en/fuck'
        url = 'http://numbersapi.com/random/year?json'
        res = task_db.delay(url=url)

        res = res.get()
        # прочитать про async, идет ожидание запроса, и оно блокирует сайт,
        # не из-за селери, а из-за того, что страница ожидает этот результат

        # запросы в базу на создание через очередь можно потом попробовать

        # потом раббит



        # r = requests.get('http://numbersapi.com/random/year?json')
        # r = requests.get('https://www.boredapi.com/api/activity/')
        # r = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/fuck')
        # r = requests.get('https://api.api-ninjas.com/v1/cars?')

        return Response(status=status.HTTP_200_OK, data=res)
