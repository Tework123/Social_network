from rest_framework import permissions

from album.models import Photo, Album


class IsAlbumCreator(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    CREATE_METHODS = ['POST']

    # для всех запросов, в том числе и post
    # не используем для проверки print здесь
    def has_permission(self, request, view):

        if request.method in self.CREATE_METHODS:
            album = Album.objects.filter(pk=view.kwargs['pk']).select_related('user')
            if album[0].user == request.user:
                return True
            else:
                return False

        if request.user.is_authenticated:
            return True
        return False

    # для всех запросов, кроме post, для get_object
    def has_object_permission(self, request, view, obj):

        # более избирательные проверки
        # if request.user.is_superuser:
        #     return True
        #
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        if obj.user == request.user:
            return True

        # if request.user.is_staff and request.method not in self.edit_methods:
        #     return True

        return False
