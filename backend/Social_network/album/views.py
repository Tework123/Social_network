from django.db.models import Prefetch, Subquery
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from album.models import Album, Photo
from album.serializers import AlbumListSerializer, PhotoListSerializer


class AlbumListView(generics.ListCreateAPIView):
    """Возвращает все альбомы по id юзера"""
    serializer_class = AlbumListSerializer

    def get_queryset(self):
        return Album.objects.filter(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        Album.objects.create(name=request.data['name'],
                             user=self.request.user)
        return Response(status=status.HTTP_201_CREATED, data='Альбом успешно добавлен')


# class AlbumEdit

class PhotoListView(generics.ListCreateAPIView):
    """Возвращает все фото по id альбома"""
    serializer_class = PhotoListSerializer

    def get_queryset(self):
        return Photo.objects.filter(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        serializer = PhotoListSerializer(request.data)
        serializer.validate(request.data)

        Photo.objects.create(image=request.data['image'],
                             text=request.data['text'],
                             album_id=self.kwargs['pk'])
        return Response(status=status.HTTP_201_CREATED, data='Фото успешно добавлено')


class PhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает, изменяет, удаляет фото по указанному id фотографии"""

    def get_queryset(self):
        return Photo.objects.filter(pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
