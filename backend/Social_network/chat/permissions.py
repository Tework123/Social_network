from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from chat.models import Chat, Message, Relationship


class IsChatUser(permissions.BasePermission):

    def has_permission(self, request, view):
        chat = get_object_or_404(Chat.objects.prefetch_related('user'), pk=view.kwargs['pk'])

        if request.user in chat.user.all():
            return True

        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsRelationshipUser(permissions.BasePermission):

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

    def has_permission(self, request, view):
        message = get_object_or_404(Message, pk=view.kwargs['pk'])
        if message.user == request.user:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True
