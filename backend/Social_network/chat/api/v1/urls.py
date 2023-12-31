from django.urls import path

from chat.api.v1.views import (ChatListView, ChatRetrieveView, RelationshipListView,
                               MessageChatListView,
                               MessageRetrieveView, MessageCreateMockChatView,
                               MessageRelationshipListView,
                               MessageCreateMockRelationshipView, RelationshipRetrieveView)

urlpatterns = [
    # чаты
    # показывает все чаты пользователя, создает чат
    path('', ChatListView.as_view()),

    # изменяет чат по pk
    path('<int:pk>/', ChatRetrieveView.as_view()),

    # показ всех сообщений чата, отправка сообщения в чат(созданного уже)(pk чата)
    path('messages/<int:pk>/', MessageChatListView.as_view({'get': 'list', 'put': 'put'})),

    # mock сообщение для чата(требуется pk чата)
    path('messages_mock/<int:pk>/', MessageCreateMockChatView.as_view()),

    # диалоги
    # показывает все диалоги, создает диалог
    path('dialogs/', RelationshipListView.as_view()),

    # изменяет диалог по pk
    path('dialogs/<int:pk>/', RelationshipRetrieveView.as_view()),

    # показ всех сообщений отношения, отправка сообщения в отношение(созданного уже)(pk отношения)
    path('dialogs/messages/<int:pk>/', MessageRelationshipListView.
         as_view({'get': 'list', 'put': 'put'})),

    # mock сообщение для отношения(требуется pk отношения)
    path('dialogs/messages_mock/<int:pk>/', MessageCreateMockRelationshipView.as_view()),

    # general
    # изменение сообщения(pk сообщения)
    path('message/<int:pk>/', MessageRetrieveView.as_view()),
]
