from django.urls import path

from chat.views import ChatListView, ChatEditView, RelationshipListView, RelationshipEditView, MessageChatListView, \
    MessageChatEditView

urlpatterns = [
    # чаты
    path('', ChatListView.as_view()),
    path('<int:pk>/', ChatEditView.as_view()),

    # показ всех сообщений чата(pk чата)
    path('messages/<int:pk>/', MessageChatListView.as_view({'get': 'list', 'post': 'post'})),

    # изменение сообщения чата(pk сообщения)
    path('message/<int:pk>/', MessageChatEditView.as_view()),

    # диалоги
    path('dialogs/', RelationshipListView.as_view()),
    path('dialogs/<int:pk>/', RelationshipEditView.as_view()),

    # все сообщения данного диалога(pk диалога)
    path('dialogs/messages/<int:pk>/', RelationshipListView.as_view()),

    # изменение конкретного сообщения(pk сообщения)
    path('dialogs/messages/<int:pk>/', RelationshipListView.as_view()),

]
