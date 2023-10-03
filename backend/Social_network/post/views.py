import json
import time

from django.db import transaction
from django.http import HttpResponse
from rest_framework import generics, status, views
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from post.models import Post
from post.serializers import PostListSerializer, PostCreateSerializer


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

        from tasks.tasks import task_db
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
        time_start = time.time()

        # надо сделать отдельное приложение, а там вьюшки с разными апишками,
        # наверное пока не делать отдельные таблицы для хранения. Просто рандом будет
        # моя задача закинуть запрос в очередь, когда вернется - показать на странице,
        # с одной апи можно сделать таблицу, для объяснения енглиш слов например, пусть будет

        # надо понять, там где то нужна авторизация, смогу ли я получить токен для апи,
        # а потом его отправлять постоянно, наверное надо при запуске приложения его получить
        #
        # потом попробуем вместо redis использовать rabbitmq, тоже самое сделаем
        # также надо гайды посмотреть по библиотеке requests, супер важно

        # digital
        # r = requests.get('http://numbersapi.com/random/year?json')
        # r = requests.get('https://www.boredapi.com/api/activity/')
        # r = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/fuck')
        # r = requests.get('https://api.api-ninjas.com/v1/cars?')
        r = requests.get("https://en.wikipedia.org/w/api.php")

        time_end = time.time()
        print(time_end - time_start)
        return Response(status=status.HTTP_200_OK, data=r.json())
