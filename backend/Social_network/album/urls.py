from django.urls import path

from album.views import AlbumListView, PhotoListView, PhotoEditView, AlbumEditView

urlpatterns = [
    # показывает все альбомы пользователя, создает альбом
    path('', AlbumListView.as_view()),

    # показывает альбом пользователя, только название, изменяет его, удаляет альбом(pk альбома)
    path('<int:pk>/', AlbumEditView.as_view()),

    # показывает все фото альбома, создает фото(требуется pk альбома)
    path('photos/<int:pk>/', PhotoListView.as_view()),

    # показывает фото альбома, изменяет(текст), удаляет его(требуется pk фото)
    path('photo/<int:pk>/', PhotoEditView.as_view()),

]
