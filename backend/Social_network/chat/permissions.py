# нужны permission для чата
# доступ к самому чату, нужна проверка перед доступом к изменению чата
# и его сообщениям - доступ для тех, кто в чате состоит(many_to_many)
#
# изменение сообщений в чате - доступ создателя
# для mock сообщения - как для обычного скорее всего
from django.db.models import Prefetch
from rest_framework import permissions

from account.models import CustomUser
from album.models import Photo, Album
from chat.models import Chat, Message


class IsChatUser(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    CREATE_METHODS = ['POST']

    # для всех запросов, в том числе и post
    # не используем для проверки print здесь
    def has_permission(self, request, view):
        # 18 sql query nice
        chat = (Chat.objects.filter(pk=view.kwargs['pk'])
                .prefetch_related(Prefetch('user',
                                           queryset=CustomUser.objects.filter(
                                               id=request.user.id))))

        if request.user in chat[0].user.all():
            return True
        # если тут блокируем get, то блокируется все остальные запросы

        return False

    # для всех запросов, кроме post и get
    def has_object_permission(self, request, view, obj):
        # if request.user in obj.user.all():
        #     return True

        return True


class IsChatUserDetail(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    CREATE_METHODS = ['POST']

    # для всех запросов, в том числе и post
    # не используем для проверки print здесь
    def has_permission(self, request, view):
        mock_message = Message.objects.filter(user=request.user,
                                              chat_id=view.kwargs['pk'], mock=True)
        if mock_message:
            return True

        chat = (Chat.objects.filter(pk=view.kwargs['pk'])
                .prefetch_related('user'))

        if request.user in chat[0].user.all():
            return True

        return False

    # для всех запросов, кроме post и get
    def has_object_permission(self, request, view, obj):

        return True
