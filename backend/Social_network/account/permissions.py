from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE", 'GET', 'POST')

    # для всех запросов, в том числе и post
    # не используем для проверки print здесь
    def has_permission(self, request, view):

        # if request.method == 'GET':
        #     return True

        # education = Education.objects.filter(user=request.user)
        # if education:
        #     return True

        # user = request.user
        # quiz = Quiz.objects.get(slug=request.resolver_match.kwargs["slug"])
        # for group in quiz.group.all():
        #     if user.groups.filter(name=group.name).exists():
        #         return True

        # стандартная проверка
        if request.user.is_authenticated:
            return True

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