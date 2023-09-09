from django.urls import path

from account.views import AccountView, AccountEditView, AccountEditEducationListView, AccountEditEducationView

urlpatterns = [

    path('im/<int:pk>/', AccountView.as_view()),

    # изменение информации об аккаунте
    path('edit/<int:pk>/', AccountEditView.as_view()),
    path('edit/education/', AccountEditEducationListView.as_view()),
    path('edit/education/<int:pk>/', AccountEditEducationView.as_view()),

]
