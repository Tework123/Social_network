from rest_framework import status, generics
from rest_framework.response import Response
from account.serializers import AccountSerializer, AccountEditSerializer, AccountEditEducationSerializer, \
    AccountEditWorkSerializer
from account.models import CustomUser, Education, Work


class AccountView(generics.RetrieveAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.kwargs['pk']).prefetch_related('education', 'work', 'groups')
        # select_related('content_type')


# надо попробовать написать свою вьюапи и сериализатор и вытащить все про пользователя
# также его друзей(relationships), группы(communa), еще посты.
class AccountEditView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountEditSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        serializer = AccountEditSerializer(request.data)
        serializer.validate(request.data)

        user = CustomUser.objects.filter(pk=self.kwargs['pk'])

        user.update(first_name=request.data['first_name'],
                    last_name=request.data['last_name'], phone=request.data['phone'],
                    city=request.data['city'], about_me=request.data['about_me'],
                    avatar=request.data['avatar'], lifestyle=request.data['lifestyle'],
                    interest=request.data['interest'], date_of_birth=request.data['date_of_birth'])

        return Response(status=status.HTTP_200_OK, data='Информация успешно изменена')


class AccountEditEducationListView(generics.ListCreateAPIView):
    """Показывает все образования, создает новое"""
    serializer_class = AccountEditEducationSerializer

    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = AccountEditEducationSerializer(request.data)
        serializer.validate(request.data)

        Education.objects.create(city=request.data['city'],
                                 name=request.data['name'],
                                 level=request.data['level'],
                                 status=request.data['status'],
                                 date_graduation=request.data['date_graduation'],
                                 user=self.request.user)

        return Response(status=status.HTTP_201_CREATED, data='Место обучения успешно добавлено')


class AccountEditEducationView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение конкретного образования"""
    serializer_class = AccountEditEducationSerializer

    def get_queryset(self):
        return Education.objects.filter(pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        serializer = AccountEditEducationSerializer(request.data)
        serializer.validate(request.data)

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

    def get_queryset(self):
        return Work.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = AccountEditWorkSerializer(request.data)
        serializer.validate(request.data)

        Work.objects.create(city=request.data['city'],
                            name=request.data['name'],
                            status=request.data['status'],
                            date_start=request.data['date_start'],
                            date_stop=request.data['date_stop'],
                            user=self.request.user)

        return Response(status=status.HTTP_201_CREATED, data='Место работы успешно добавлено')


class AccountEditWorkView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение конкретного образования"""
    serializer_class = AccountEditWorkSerializer

    def get_queryset(self):
        return Work.objects.filter(pk=self.kwargs['pk'])

    def put(self, request, *args, **kwargs):
        serializer = AccountEditWorkSerializer(request.data)
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
