from django.urls import path

from account.views import AccountView, AccountEditView, AccountEditEducationListView, AccountEditEducationView, \
    AccountEditWorkListView, AccountEditWorkView, AccountEditAvatarView

urlpatterns = [

    # показывает информация об аккаунте
    path('im/', AccountView.as_view()),

    # изменение информации об аккаунте
    # изменение текстовых полей
    path('edit/', AccountEditView.as_view()),

    # изменение аватара
    path('edit/avatar/', AccountEditAvatarView.as_view()),

    # показывает все образования, создает образование
    path('edit/education/', AccountEditEducationListView.as_view()),

    # изменение образования, требуется pk образования
    path('edit/education/<int:pk>/', AccountEditEducationView.as_view()),

    # показывает все работы, создает работу
    path('edit/work/', AccountEditWorkListView.as_view()),

    # изменение работы, требуется pk работы
    path('edit/work/<int:pk>/', AccountEditWorkView.as_view()),

]
