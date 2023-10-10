from django.urls import path

from album.api.v1.views import AlbumListView, PhotoListView, AlbumRetrieveView, PhotoRetrieveView

urlpatterns = [
    # показывает все альбомы пользователя, создает альбом
    path('', AlbumListView.as_view()),

    # показывает альбом пользователя, только название, изменяет его, удаляет альбом(pk альбома)
    path('<int:pk>/', AlbumRetrieveView.as_view()),

    # показывает все фото альбома, создает фото(требуется pk альбома)
    path('photos/<int:pk>/', PhotoListView.as_view()),

    # показывает фото альбома, изменяет(текст), удаляет его(требуется pk фото)
    path('photo/<int:pk>/', PhotoRetrieveView.as_view()),

]
