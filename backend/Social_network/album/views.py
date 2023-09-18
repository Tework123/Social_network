from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from album.models import Album, Photo
from album.permissions import IsAlbumCreator
from album.serializers import AlbumListSerializer, PhotoListSerializer, PhotoDetailSerializer, \
    PhotoChangeDetailSerializer, AlbumEditSerializer


class AlbumListView(generics.ListCreateAPIView):
    """Показывает все альбомы пользователя вместе с первым фото каждого,
     создает альбом"""
    serializer_class = AlbumListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Album.objects.filter(user=self.request.user).
                prefetch_related('photo').order_by('date_create'))

    def post(self, request, *args, **kwargs):
        Album.objects.create(name=request.data['name'],
                             user=self.request.user)
        return Response(status=status.HTTP_201_CREATED, data='Альбом успешно добавлен')


class AlbumEditView(generics.RetrieveUpdateDestroyAPIView):
    """Изменяет название альбома"""
    serializer_class = AlbumEditSerializer
    permission_classes = [IsAuthenticated, IsAlbumCreator]

    def get_object(self):
        return get_object_or_404(Album, pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        album = Album.objects.filter(pk=self.kwargs['pk'])
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
    serializer_class = PhotoListSerializer
    permission_classes = [IsAuthenticated, IsAlbumCreator]

    def get_queryset(self):
        return Photo.objects.filter(album_photo=self.kwargs['pk']).order_by('-date_create')

    def post(self, request, *args, **kwargs):
        serializer = PhotoListSerializer(request.data)
        serializer.validate(request.data)

        photo = Photo.objects.create(image=request.data['image'],
                                     text=request.data['text'],
                                     user=self.request.user)

        album = get_object_or_404(Album, id=self.kwargs['pk'])
        album.photo.add(photo)

        return Response(status=status.HTTP_201_CREATED, data='Фото успешно добавлено')


class PhotoEditView(viewsets.ViewSet):
    """Показывает, изменяет, удаляет фото по id фотографии"""
    permission_classes = [IsAuthenticated, IsAlbumCreator]

    def get(self, request, pk=None):
        photo = get_object_or_404(Photo, pk=pk)
        serializer = PhotoDetailSerializer(photo)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, pk=None):
        photo = get_object_or_404(Photo, pk=pk)

        serializer = PhotoChangeDetailSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data='Фото изменено успешно')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        photo = get_object_or_404(Photo, pk=pk)
        photo.delete()
        return Response(status=status.HTTP_200_OK, data='Фото удалено успешно')
