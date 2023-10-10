import datetime
from faker import Faker
from django.test import TestCase
from rest_framework import status
from account.models import CustomUser, Work, Education

fake = Faker()


class AccountViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """Заполняет данными базу"""

        user = CustomUser.objects.create_user(email='user@mail.ru',
                                              password='user@mail.ru', is_active=True)

        for i in range(3):
            work_name = fake.company()
            Work.objects.create(name=work_name, user=user)

        for i in range(2):
            education_name = fake.company()
            Education.objects.create(name=education_name, user=user)

    def setUp(self) -> None:
        """Авторизует пользователя перед каждым тестом"""

        self.client.login(email='user@mail.ru',
                          password='user@mail.ru')

    @staticmethod
    def get_user() -> CustomUser:
        """Возвращает тестового пользователя"""

        user = CustomUser.objects.get(email='user@mail.ru')
        return user

    def test_account(self):
        response = self.client.get('/v1/account/im/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_edit(self):
        response = self.client.patch('/v1/account/edit/',
                                     data={'first_name': '',
                                           'last_name': '',
                                           'phone': '',
                                           'city': '',
                                           'about_me': '',
                                           'lifestyle': '',
                                           'interest': '',
                                           'date_of_birth': datetime.date.today()},
                                     content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Информация успешно изменена')

    def test_account_edit_avatar(self):
        response = self.client.post('/v1/account/edit/avatar/',
                                    data={'avatar': '',
                                          },
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_account_work(self):
        response = self.client.get('/v1/account/edit/work/')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_work_create(self):
        response = self.client.post('/v1/account/edit/work/',
                                    data={'name': 'traktorist',
                                          'city': '',
                                          'status': '',
                                          'date_start': None,
                                          'date_stop': None,
                                          'user': self.get_user().id},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Место работы успешно добавлено')

    def test_account_work_edit(self):
        response = self.client.patch('/v1/account/edit/work/1/',
                                     data={'name': 'traktorist',
                                           'city': 'Moscow',
                                           'status': '',
                                           'date_start': datetime.date.today(),
                                           'date_stop': datetime.date.today(),
                                           'user': self.get_user().id},
                                     content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Информация успешно изменена')

    def test_account_work_delete(self):
        response = self.client.delete('/v1/account/edit/work/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/v1/account/edit/work/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get('/v1/account/edit/work/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_account_education(self):
        response = self.client.get('/v1/account/edit/education/')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_education_create(self):
        response = self.client.post('/v1/account/edit/education/',
                                    data={'name': 'school',
                                          'city': '',
                                          'status': '',
                                          'level': '',
                                          'date_graduation': None,
                                          'user': self.get_user().id},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Место обучения успешно добавлено')

    def test_account_education_edit(self):
        response = self.client.patch('/v1/account/edit/education/1/',
                                     data={'name': 'school',
                                           'city': 'Moscow',
                                           'status': '',
                                           'level': '',
                                           'date_graduation': datetime.date.today(),
                                           'user': self.get_user().id},
                                     content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Информация успешно изменена')

    def test_account_education_delete(self):
        self.client.delete('/v1/account/edit/education/1/')

        response = self.client.get('/v1/account/edit/education/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get('/v1/account/edit/education/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
