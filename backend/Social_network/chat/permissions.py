from rest_framework import permissions
from rest_framework.generics import get_object_or_404
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


class IsRelationshipUser(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    CREATE_METHODS = ['POST']

    def has_permission(self, request, view):
        relationship = get_object_or_404(Relationship.objects
                                         .select_related('user_1', 'user_2'),
                                         pk=view.kwargs['pk'])

        if request.user == relationship.user_1 or request.user == relationship.user_2:
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
