from django.urls import path

from album.views import AlbumListView, PhotoListView

urlpatterns = [

    path('<int:pk>/', AlbumListView.as_view()),
    path('photos/<int:pk>/', PhotoListView.as_view()),

]
