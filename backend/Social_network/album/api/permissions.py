from rest_framework import permissions

from album.models import Album


class IsAlbumCreator(permissions.BasePermission):
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
    CREATE_METHODS = ['POST']

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

    def has_object_permission(self, request, view, obj):

        if obj.user == request.user:
            return True

        return False
