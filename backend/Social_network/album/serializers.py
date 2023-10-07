from rest_framework import serializers
from album.models import Album, Photo


class AlbumListGETSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('last_photo')

    def last_photo(self, obj):
        last_photo = Photo.objects.filter(album_photo=obj.pk).order_by('date_create')[:1]
        return PhotoListGETSerializer(last_photo, many=True).data

    class Meta:
        model = Album
        fields = ['id',
                  'name',
                  'photo']


class AlbumPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['name']


class AlbumRetrieveGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id',
                  'name']


class PhotoListGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id',
                  'image',
                  'text',
                  'date_create']


class PhotoPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image',
                  'text']


class PhotoRetrieveGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id',
                  'image',
                  'text']


class PhotoRetrievePATCHSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['text']
