from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from album.models import Album, Photo


class AlbumListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('last_photo')

    def last_photo(self, obj):
        # здесь нужен order_by по дате добавления фото
        last_photo = Photo.objects.filter(album_photo=obj.pk).order_by('date_create')[:1]
        return PhotoListSerializer(last_photo, many=True).data

    class Meta:
        model = Album
        fields = ['id', 'name', 'photo']


class AlbumEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name']


class PhotoListSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        attrs._mutable = True

        if attrs['image'] == '':
            raise ValidationError('Фото должно быть добавлено')

        return attrs

    class Meta:
        model = Photo
        fields = ['id', 'image', 'text']


class PhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'text']


class PhotoChangeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'text']
