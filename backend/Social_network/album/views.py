from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from album.models import Album, Photo
from album.permissions import IsAlbumCreator
from album.serializers import (AlbumListSerializer, PhotoListSerializer,
                               PhotoEditGetSerializer,
                               PhotoEditPutSerializer, AlbumEditSerializer, PhotoCreateSerializer)


class AlbumListView(generics.ListCreateAPIView):
    """Показывает все альбомы пользователя вместе с первым фото каждого,
     создает альбом"""
    serializer_class = AlbumListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Album.objects.filter(user=self.request.user).
                prefetch_related('photo').order_by('date_create'))

    def post(self, request, *args, **kwargs):
        serializer = AlbumListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Album.objects.create(name=request.data['name'],
                             user=self.request.user)
        return Response(status=status.HTTP_201_CREATED, data='Альбом успешно добавлен')


class AlbumEditView(generics.RetrieveUpdateDestroyAPIView):
    """Изменяет название альбома"""
    permission_classes = [IsAuthenticated, IsAlbumCreator]
    serializer_class = AlbumEditSerializer

    def get_object(self):
        return get_object_or_404(Album, pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        serializer = AlbumEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        album = Album.objects.filter(pk=self.kwargs['pk'])

        if album[0].avatar_album:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data='Альбом с фото профиля нельзя переименовать')

        album.update(name=request.data['name'])
        return Response(status=status.HTTP_200_OK, data='Альбом успешно изменен')

    def delete(self, request, *args, **kwargs):
        album = Album.objects.filter(pk=self.kwargs['pk'])
        if album[0].avatar_album:
            return Response(status=status.HTTP_200_OK, data='Альбом с фото профиля нельзя удалить')

        album.delete()
        return Response(status=status.HTTP_200_OK, data='Альбом успешно удален')


class PhotoListView(generics.ListCreateAPIView):
    """Показывает все фото по id альбома, создает фото"""
    permission_classes = [IsAuthenticated, IsAlbumCreator]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PhotoListSerializer
        else:
            return PhotoCreateSerializer

    def get_queryset(self):
        return Photo.objects.filter(album_photo=self.kwargs['pk']).order_by('-date_create')

    def post(self, request, *args, **kwargs):
        serializer = PhotoListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        photo = Photo.objects.create(image=request.data['image'],
                                     text=request.data['text'],
                                     user=self.request.user,
                                     )

        album = get_object_or_404(Album, id=self.kwargs['pk'])
        album.photo.add(photo)

        return Response(status=status.HTTP_201_CREATED, data='Фото успешно добавлено')


class PhotoEditView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает, изменяет, удаляет фото по id фотографии"""
    permission_classes = [IsAuthenticated, IsAlbumCreator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PhotoEditGetSerializer
        else:
            return PhotoEditPutSerializer

    def get_object(self):
        return get_object_or_404(Photo, pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        serializer = PhotoEditPutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        photo = Photo.objects.filter(pk=self.kwargs['pk'])

        photo.update(text=request.data['text'])

        return Response(status=status.HTTP_200_OK, data='Фото изменено успешно')

    def delete(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])

        # удаляет только фото из файлового хранилища
        photo.image.delete(save=True)

        # удаляет только ссылку на фото из базы данных
        photo.delete()
        return Response(status=status.HTTP_200_OK, data='Фото удалено успешно')
