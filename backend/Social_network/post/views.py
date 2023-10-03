from django.db import transaction
from rest_framework import generics, status
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
                transaction.on_commit(lambda: task_db.delay(job_params))
        except Exception as e:
            raise APIException(str(e))
        # serializer.save()

        return Response(status=status.HTTP_201_CREATED, data='Пост успешно создан')


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
