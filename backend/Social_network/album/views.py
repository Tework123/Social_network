from django.shortcuts import render
from rest_framework import generics

from album.models import Album
from album.serializers import AlbumListSerializer


class GetAlbums(generics.ListAPIView):
    serializer_class = AlbumListSerializer
    queryset = Album.objects.all()
