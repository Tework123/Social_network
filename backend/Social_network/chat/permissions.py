# нужны permission для чата
# доступ к самому чату, нужна проверка перед доступом к изменению чата
# и его сообщениям - доступ для тех, кто в чате состоит(many_to_many)
#
# изменение сообщений в чате - доступ создателя
# для mock сообщения - как для обычного скорее всего
from django.db.models import Prefetch
from rest_framework import permissions
from account.models import CustomUser
from chat.models import Chat, Message, Relationship


class IsChatUser(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    CREATE_METHODS = ['POST']

    # для всех запросов, в том числе и post
    # не используем для проверки print здесь
    def has_permission(self, request, view):
        # 18 sql query nice
        # select_related для fk
        chat = (Chat.objects.filter(pk=view.kwargs['pk'])
                .prefetch_related(Prefetch('user',
                                           queryset=CustomUser.objects.filter(
                                               id=request.user.id))))


        #chat = get_or_404
        # починить, наверное надо везде поменять на get_or_404, чтобы выдавало ошибку
        # когда нет сущности, а не пыталось получить к ней доступ
        print(chat)
        print(chat)
        print(chat)
        print(chat)

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
        message = Message.objects.filter(pk=view.kwargs['pk'], user=request.user)
        if message:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # if obj.user == request.user:
        #     return True

        return True
