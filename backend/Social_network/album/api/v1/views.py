from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from album.models import Album, Photo
from album.api.permissions import IsAlbumCreator
from album.api.serializers import (
    AlbumPOSTSerializer, AlbumRetrieveGETSerializer,
    PhotoPOSTSerializer,
    PhotoRetrievePATCHSerializer, PhotoRetrieveGETSerializer,
    AlbumListGETSerializer, PhotoListGETSerializer)


class AlbumListView(generics.ListCreateAPIView):
    """Показывает все альбомы пользователя вместе с первым фото каждого,
     создает альбом"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AlbumListGETSerializer
        else:
            return AlbumPOSTSerializer

    def get_queryset(self):
        return (Album.objects.filter(user=self.request.user).
                prefetch_related('photo').order_by('date_create'))

    def post(self, request, *args, **kwargs):
        serializer = AlbumPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response(status=status.HTTP_201_CREATED, data='Альбом успешно добавлен')


class AlbumRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменяет название альбома"""
    permission_classes = [IsAuthenticated, IsAlbumCreator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AlbumRetrieveGETSerializer
        else:
            return AlbumPOSTSerializer

    def get_object(self):
        return get_object_or_404(Album, pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        album = Album.objects.filter(pk=self.kwargs['pk'])
        if album[0].avatar_album:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data='Альбом с фото профиля нельзя переименовать')

        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Альбом успешно изменен')

    def delete(self, request, *args, **kwargs):
        album = Album.objects.filter(pk=self.kwargs['pk'])
        if album[0].avatar_album:
            return Response(status=status.HTTP_200_OK,
                            data='Альбом с фото профиля нельзя удалить')

        album.delete()

        return Response(status=status.HTTP_200_OK, data='Альбом успешно удален')


class PhotoListView(generics.ListCreateAPIView):
    """Показывает все фото по id альбома, создает фото"""
    permission_classes = [IsAuthenticated, IsAlbumCreator]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PhotoListGETSerializer
        else:
            return PhotoPOSTSerializer

    def get_queryset(self):
        return Photo.objects.filter(album_photo=self.kwargs['pk']).order_by('-date_create')

    def post(self, request, *args, **kwargs):
        serializer = PhotoPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo = serializer.save(user=self.request.user)

        album = get_object_or_404(Album, id=self.kwargs['pk'])
        album.photo.add(photo)

        return Response(status=status.HTTP_201_CREATED, data='Фото успешно добавлено')


class PhotoRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Показывает, изменяет, удаляет фото по id фотографии"""
    permission_classes = [IsAuthenticated, IsAlbumCreator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PhotoRetrieveGETSerializer
        else:
            return PhotoRetrievePATCHSerializer

    def get_object(self):
        return get_object_or_404(Photo, pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Фото изменено успешно')

    def delete(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])

        # удаляет только фото из файлового хранилища
        photo.image.delete(save=True)

        # удаляет только ссылку на фото из базы данных
        photo.delete()
        return Response(status=status.HTTP_200_OK, data='Фото удалено успешно')
