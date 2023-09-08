from django.urls import path

from account.views import AccountView

urlpatterns = [

    path('<int:pk>/', AccountView.as_view()),

]
