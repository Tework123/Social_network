# нужны permission для чата
# доступ к самому чату, нужна проверка перед доступом к изменению чата
# и его сообщениям - доступ для тех, кто в чате состоит(many_to_many)
#
# изменение сообщений в чате - доступ создателя
# для mock сообщения - как для обычного скорее всего
from django.db.models import Prefetch
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from account.models import CustomUser
from chat.models import Chat, Message, Relationship


class IsChatUser(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    CREATE_METHODS = ['POST']

    # для всех запросов, в том числе и post
    # не используем для проверки print здесь
    def has_permission(self, request, view):
        # chat = (Chat.objects.filter(pk=view.kwargs['pk'])
        #         .prefetch_related(Prefetch('user',
        #                                    queryset=CustomUser.objects.filter(
        #                                        id=request.user.id))))

        chat = get_object_or_404(Chat.objects.prefetch_related('user'), pk=view.kwargs['pk'])

        if request.user in chat.user.all():
            return True
        # если тут блокируем get, то блокируется все остальные запросы

        return False

    # для всех запросов, кроме post и get
    def has_object_permission(self, request, view, obj):
        # if request.user in obj.user.all():
        #     return True

        return True


# зачем это?
# надо диалоги переделать, потом тесты и селери
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


class IsRelationshipUser(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    CREATE_METHODS = ['POST']

    def has_permission(self, request, view):
        relationship = Relationship.objects.filter(pk=view.kwargs['pk']).select_related('user_1', 'user_2')

        if request.user == relationship[0].user_1 or request.user == relationship[0].user_2:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsMessageCreator(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    CREATE_METHODS = ['POST']

    def has_permission(self, request, view):
        get_object_or_404(Message, pk=view.kwargs['pk'], user=request.user)
        return True

    def has_object_permission(self, request, view, obj):
        return True
