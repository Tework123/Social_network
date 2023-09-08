from django.urls import path

from account.views import AccountView, AccountEditView

urlpatterns = [

    path('im/<int:pk>/', AccountView.as_view()),
    path('edit/<int:pk>/', AccountEditView.as_view()),

]
