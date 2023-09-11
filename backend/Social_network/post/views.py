from django.shortcuts import render
from rest_framework import generics

from post.models import Post
from post.serializers import PostListSerializer


class GetPosts(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
