from rest_framework import permissions

from account.models import Education


class IsCreator(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE", 'GET', 'POST')

    # надо  чтобы удаление тоже не работало, почекать статью
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        # education = Education.objects.filter(user=request.user)
        # if education:
        #     return True

        # user = request.user
        # quiz = Quiz.objects.get(slug=request.resolver_match.kwargs["slug"])
        # for group in quiz.group.all():
        #     if user.groups.filter(name=group.name).exists():
        #         return True

        # стандартная проверка
        # if request.user.is_authenticated:
        #     print('123')
        #     return True

    def has_object_permission(self, request, view, obj):

        # более избирательные проверки
        # if request.user.is_superuser:
        #     return True
        #
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        if obj.user == request.user:
            print(obj.user)
            return True

        # if request.user.is_staff and request.method not in self.edit_methods:
        #     return True

        return False
