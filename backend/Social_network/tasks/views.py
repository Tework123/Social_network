import time

import requests
from django.db import transaction
from rest_framework import generics, status, views
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tasks.tasks import task_db, test_task

from post.models import Post
from post.serializers import PostListSerializer, PostCreateSerializer

import logging

log = logging.getLogger(__name__)


class CreatePostTransactionView(generics.ListCreateAPIView):
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
        serializer = PostCreateSerializer(data=request.data, context={'user': self.request.user})
        serializer.is_valid(raise_exception=True)

        # если происходит ошибка внутри блока - откатываются все операции блока
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

        return Response(status=status.HTTP_201_CREATED, data=f'Пост успешно создан,'
                                                             f'res={task.status}')


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
        serializer = PostCreateSerializer(data=request.data, context={'user': self.request.user})
        serializer.is_valid(raise_exception=True)

        # То же самое, что и сверху, но без блока транзакции
        instance = serializer.save()

        job_params = {"id": instance.id}

        task = task_db.delay(job_params)

        return Response(status=status.HTTP_201_CREATED, data=f'Пост успешно создан,'
                                                             f'res={task.status}')


class PostEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostCreateSerializer

    def get_queryset(self):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        Post.objects.all().delete()
        return Response(status=status.HTTP_200_OK, data='Пост успешно удален')


class DigitalAPiView(views.APIView):

    # пытаемся оправить асинхронный запрос на внешний апи
    # он даже без библиотеки не блокирует приложение, ничего не понял, ну ладно
    def get(self, request):
        url = 'http://numbersapi.com/random/year?json'
        res = requests.get(url=url)
        time.sleep(5)

        # r = requests.get('http://numbersapi.com/random/year?json')
        # r = requests.get('https://www.boredapi.com/api/activity/')
        # english
        # r = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/fuck')
        # food
        # https: // spoonacular.com / food - api / pricing
        # a lot of api, need token
        # r = requests.get('https://api.api-ninjas.com/v1/cars?')

        return Response(status=status.HTTP_200_OK, data=res.json())


class RedisTestView(views.APIView):

    def get(self, request):
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en/fuck'
        res = test_task.delay(url)
        res = res.get()
        return Response(status=status.HTTP_200_OK, data=res[0])
