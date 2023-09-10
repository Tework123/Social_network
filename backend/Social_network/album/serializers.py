from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from album.models import Album, Photo


class AlbumListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('last_photo')

    def last_photo(self, obj):
        # здесь нужен order_by по дате добавления фото
        last_photo = Photo.objects.filter(album_id=obj.pk)[:1]
        return PhotoListSerializer(last_photo, many=True).data

    class Meta:
        model = Album
        fields = ['name', 'photo']


class PhotoListSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        attrs._mutable = True

        if attrs['image'] == '':
            raise ValidationError('Фото должно быть добавлено')

        return attrs

    class Meta:
        model = Photo
        fields = ['image', 'text']
