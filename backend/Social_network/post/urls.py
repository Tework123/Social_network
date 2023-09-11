from django.urls import path

from post.views import GetPosts

urlpatterns = [

    path('', GetPosts.as_view()),

]
