from django.urls import path

from chat.views import ChatListView, ChatEditView

urlpatterns = [

    path('', ChatListView.as_view()),
    path('<int:pk>/', ChatEditView.as_view()),

]
