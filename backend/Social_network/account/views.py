from rest_framework import status, generics, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.permissions import IsCreator
from account.serializers import (CustomUserSerializer, CustomUserEditGETSerializer,
                                 CustomUserEditPATCHSerializer,
                                 CustomUserEditAvatarSerializer,
                                 EducationGETSerializer, WorkGETSerializer,
                                 WorkPOSTSerializer,
                                 EducationPOSTSerializer)
from account.models import CustomUser, Education, Work
from album.models import Album, Photo


class CustomUserRetrieveView(generics.RetrieveAPIView):
    """Показывает информацию о пользователе"""
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(CustomUser.objects
                                 .prefetch_related('education', 'work'),
                                 id=self.request.user.id)


class CustomUserRetrieveEditView(generics.RetrieveUpdateAPIView):
    """Обновляет основные текстовые поля пользователя"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return CustomUserEditGETSerializer
        else:
            return CustomUserEditPATCHSerializer

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Информация успешно изменена')


class CustomUserEditAvatarView(generics.CreateAPIView):
    """Обновляет фото аватара, добавляет предыдущие фото аватара в отдельный альбом"""
    serializer_class = CustomUserEditAvatarSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserEditAvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomUser.objects.filter(id=self.request.user.id)

        try:
            avatar_album = Album.objects.get(user=user[0], avatar_album=True)
        except Exception as e:
            avatar_album = Album.objects.create(name='Фото профиля', avatar_album=True,
                                                user=user[0])

        photo = Photo.objects.create(image=request.data['avatar'], user=user[0])
        avatar_album.photo.add(photo)

        user.update(avatar=request.data['avatar'])

        return Response(status=status.HTTP_200_OK, data='Фото профиля успешно изменено')


class EducationListView(generics.ListCreateAPIView):
    """Показывает все образования, создает новое"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EducationGETSerializer
        else:
            return EducationPOSTSerializer

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = EducationPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response(status=status.HTTP_201_CREATED, data='Место обучения успешно добавлено')


class EducationRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменяет конкретное образование"""
    permission_classes = [IsAuthenticated, IsCreator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EducationGETSerializer
        else:
            return EducationPOSTSerializer

    def get_object(self):
        return get_object_or_404(Education, pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Информация успешно изменена')

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Образование удалено успешно')


class WorkListView(generics.ListCreateAPIView):
    """Показывает все места работы, создает новое"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkGETSerializer
        else:
            return WorkPOSTSerializer

    def get_queryset(self):
        return Work.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = WorkPOSTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response(status=status.HTTP_201_CREATED, data='Место работы успешно добавлено')


class WorkRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменяет конкретное место работы"""
    permission_classes = [IsAuthenticated, IsCreator]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkGETSerializer
        else:
            return WorkPOSTSerializer

    def get_object(self):
        return get_object_or_404(Work, pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Информация успешно изменена')

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Образование удалено успешно')
