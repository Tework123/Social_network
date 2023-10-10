from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE", 'GET', 'POST')

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):

        if obj.user == request.user:
            return True

        return False
