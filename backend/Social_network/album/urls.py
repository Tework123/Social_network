from django.urls import path

from album.views import AlbumListView, PhotoListView, PhotoDetailView, AlbumEditView

urlpatterns = [

    path('<int:pk>/', AlbumListView.as_view()),
    path('album/<int:pk>/', AlbumEditView.as_view()),
    path('photos/<int:pk>/', PhotoListView.as_view()),
    path('photo/<int:pk>/', PhotoDetailView.as_view({'get': 'get', 'put': 'put', 'delete': 'delete'})),

]
