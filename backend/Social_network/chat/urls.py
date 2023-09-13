from django.urls import path

from chat.views import ChatListView, ChatEditView, RelationshipListView, RelationshipEditView, MessageChatListView, \
    MessageChatEditView, MessageCreateMockChatView, AttachPhotoMessageMockView

urlpatterns = [
    # чаты
    path('', ChatListView.as_view()),
    path('<int:pk>/', ChatEditView.as_view()),

    # показ всех сообщений чата(pk чата)
    path('messages/<int:pk>/', MessageChatListView.as_view({'get': 'list', 'post': 'post'})),

    # изменение сообщения чата(pk сообщения)
    path('message/<int:pk>/', MessageChatEditView.as_view()),

    # mock сообщение для чата(требуется pk чата)
    path('messages_mock/<int:pk>/', MessageCreateMockChatView.as_view()),

    # добавление фото для сообщения mock=True(требуется pk сообщения)
    path('messages_mock_image/<int:pk>/', AttachPhotoMessageMockView.as_view()),

    ########
    # диалоги
    path('dialogs/', RelationshipListView.as_view()),
    path('dialogs/<int:pk>/', RelationshipEditView.as_view()),

    # все сообщения данного диалога(pk диалога)
    path('dialogs/messages/<int:pk>/', RelationshipListView.as_view()),

    # изменение конкретного сообщения(pk сообщения)
    path('dialogs/messages/<int:pk>/', RelationshipListView.as_view()),

]
