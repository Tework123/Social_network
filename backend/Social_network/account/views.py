from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.permissions import IsCreator
from account.serializers import (AccountSerializer, AccountEditSerializer,
                                 AccountEditEducationSerializer,
                                 AccountEditWorkSerializer, AccountEditAvatarSerializer)
from account.models import CustomUser, Education, Work
from album.models import Album, Photo


class AccountView(generics.RetrieveAPIView):
    """Показывает информацию о пользователе"""
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    # не могу вытащить relationship, потому что там user_1, а не user
    # альбомы будет сложно подцепить, да и нужно ли это
    # надо подцепить посты и группы
    def get_object(self):
        return get_object_or_404(CustomUser.objects
                                 .prefetch_related('education', 'work'),
                                 id=self.request.user.id)


class AccountEditView(generics.RetrieveUpdateAPIView):
    """Обновляет основные текстовые поля пользователя"""
    serializer_class = AccountEditSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.request.user.id)

    def put(self, request, *args, **kwargs):
        serializer = AccountEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomUser.objects.filter(id=self.request.user.id)

        user.update(first_name=request.data['first_name'],
                    last_name=request.data['last_name'], phone=request.data['phone'],
                    city=request.data['city'], about_me=request.data['about_me'],
                    lifestyle=request.data['lifestyle'],
                    interest=request.data['interest'], date_of_birth=request.data['date_of_birth'])

        return Response(status=status.HTTP_200_OK, data='Информация успешно изменена')


class AccountEditAvatarView(generics.CreateAPIView):
    """Обновляет фото аватара, добавляет предыдущие фото аватара в отдельный альбом"""
    serializer_class = AccountEditAvatarSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AccountEditAvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomUser.objects.filter(id=self.request.user.id)

        try:
            avatar_album = Album.objects.get(user=user[0], avatar_album=True)
        except:
            avatar_album = Album.objects.create(name='Фото профиля', avatar_album=True,
                                                user=user[0])

        photo = Photo.objects.create(image=request.data['avatar'], user=user[0])

        avatar_album.photo.add(photo)

        user.update(avatar=request.data['avatar'])

        return Response(status=status.HTTP_200_OK, data='Фото профиля успешно изменено')


class AccountEditEducationListView(generics.ListCreateAPIView):
    """Показывает все образования, создает новое"""
    serializer_class = AccountEditEducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = AccountEditEducationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Education.objects.create(city=request.data['city'],
                                 name=request.data['name'],
                                 level=request.data['level'],
                                 status=request.data['status'],
                                 date_graduation=request.data['date_graduation'],
                                 user=self.request.user)

        return Response(status=status.HTTP_201_CREATED, data='Место обучения успешно добавлено')


class AccountEditEducationView(generics.RetrieveUpdateDestroyAPIView):
    """Изменяет конкретное образование"""
    serializer_class = AccountEditEducationSerializer
    permission_classes = [IsAuthenticated, IsCreator]

    def get_object(self):
        return get_object_or_404(Education, pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        serializer = AccountEditEducationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        education = Education.objects.filter(pk=self.kwargs['pk'])

        education.update(name=request.data['name'],
                         city=request.data['city'],
                         date_graduation=request.data['date_graduation'],
                         status=request.data['status'],
                         level=request.data['level'])

        return Response(status=status.HTTP_200_OK, data='Информация успешно изменена')

    def delete(self, request, *args, **kwargs):
        Education.objects.filter(pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_200_OK, data='Образование удалено успешно')


class AccountEditWorkListView(generics.ListCreateAPIView):
    """Показывает все места работы, создает новое"""
    serializer_class = AccountEditWorkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Work.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = AccountEditWorkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validate(request.data)

        Work.objects.create(city=request.data['city'],
                            name=request.data['name'],
                            status=request.data['status'],
                            date_start=request.data['date_start'],
                            date_stop=request.data['date_stop'],
                            user=self.request.user)

        return Response(status=status.HTTP_201_CREATED, data='Место работы успешно добавлено')


class AccountEditWorkView(generics.RetrieveUpdateDestroyAPIView):
    """Изменяет конкретное место работы"""
    serializer_class = AccountEditWorkSerializer
    permission_classes = [IsAuthenticated, IsCreator]

    def get_object(self):
        return get_object_or_404(Work, pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        serializer = AccountEditWorkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validate(request.data)

        education = Work.objects.filter(pk=self.kwargs['pk'])

        education.update(city=request.data['city'],
                         name=request.data['name'],
                         status=request.data['status'],
                         date_start=request.data['date_start'],
                         date_stop=request.data['date_stop'],
                         user=self.request.user)

        return Response(status=status.HTTP_200_OK, data='Информация успешно изменена')

    def delete(self, request, *args, **kwargs):
        Work.objects.filter(pk=self.kwargs['pk']).delete()
        return Response(status=status.HTTP_200_OK, data='Образование удалено успешно')
