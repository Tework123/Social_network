from django.urls import path

from album.views import GetAlbums

urlpatterns = [

    path('', GetAlbums.as_view()),

]
