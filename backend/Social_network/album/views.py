from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from album.models import Album, Photo
from album.serializers import AlbumListSerializer, PhotoListSerializer, PhotoDetailSerializer, \
    PhotoChangeDetailSerializer, AlbumEditSerializer


class AlbumListView(generics.ListCreateAPIView):
    """Возвращает все альбомы по id юзера"""
    serializer_class = AlbumListSerializer

    def get_queryset(self):
        return Album.objects.filter(pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        Album.objects.create(name=request.data['name'],
                             user=self.request.user)
        return Response(status=status.HTTP_201_CREATED, data='Альбом успешно добавлен')


class AlbumEditView(generics.RetrieveUpdateDestroyAPIView):
    """Изменяет параметры альбома"""
    serializer_class = AlbumEditSerializer

    # get не нужен здесь
    def get_queryset(self):
        return Album.objects.filter(pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        album = get_object_or_404(Album, pk=self.kwargs['pk'])
        album.update(name=request.data['name'])
        return Response(status=status.HTTP_200_OK, data='Альбом успешно изменен')

    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK, data='Альбом успешно удален')


class PhotoListView(generics.ListCreateAPIView):
    """Возвращает все фото по id альбома, создает фото"""
    serializer_class = PhotoListSerializer

    def get_queryset(self):
        return Photo.objects.filter(album_id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        serializer = PhotoListSerializer(request.data)
        serializer.validate(request.data)

        Photo.objects.create(image=request.data['image'],
                             text=request.data['text'],
                             album_id=self.kwargs['pk'])
        return Response(status=status.HTTP_201_CREATED, data='Фото успешно добавлено')


class PhotoDetailView(viewsets.ViewSet):
    """Показывает, изменяет, удаляет фото по указанному id фотографии"""

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
