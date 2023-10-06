from django.urls import path

from account.views import (CustomUserRetrieveView, CustomUserRetrieveEditView,
                           CustomUserEditAvatarView,
                           EducationListView, EducationRetrieveView,
                           WorkListView, WorkRetrieveView)

urlpatterns = [

    # показывает информация об аккаунте
    path('im/', CustomUserRetrieveView.as_view()),

    # изменение информации об аккаунте
    # изменение текстовых полей
    path('edit/', CustomUserRetrieveEditView.as_view()),

    # изменение аватара
    path('edit/avatar/', CustomUserEditAvatarView.as_view()),

    # показывает все образования, создает образование
    path('edit/education/', EducationListView.as_view()),

    # изменение образования, требуется pk образования
    path('edit/education/<int:pk>/', EducationRetrieveView.as_view()),

    # показывает все работы, создает работу
    path('edit/work/', WorkListView.as_view()),

    # изменение работы, требуется pk работы
    path('edit/work/<int:pk>/', WorkRetrieveView.as_view()),

]
