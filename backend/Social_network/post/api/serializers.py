from rest_framework import serializers

from post.models import Post


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        photos = validated_data.pop('photo', None)

        post = Post.objects.create(user=self.context['user'], **validated_data)

        if photos:
            for photo in photos:
                post.photo.add(photo)

        return post

    class Meta:
        model = Post
        fields = ['text', 'photo']
