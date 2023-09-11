from django.urls import path

from chat.views import GetChats

urlpatterns = [

    path('', GetChats.as_view()),

]
