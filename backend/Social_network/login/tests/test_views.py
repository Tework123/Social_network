from django.core import mail
from django.test import TestCase
from faker import Faker
from rest_framework import status
from account.models import CustomUser

fake = Faker()


class LoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """Заполняет данными базу"""
        CustomUser.objects.create_user(email='user1@mail.ru',
                                       password='user1@mail.ru', is_active=True)

        CustomUser.objects.create_user(email='user2@mail.ru',
                                       password='user2@mail.ru', is_active=False)

    def setUp(self) -> None:
        pass

    def test_account_create_already_exist(self):
        response = self.client.post('/api/v1/login/register/',
                                    data={'email': 'user1@mail.ru',
                                          'password': '123123123'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_account_create(self):
        response = self.client.post('/api/v1/login/register/',
                                    data={'email': 'user3@mail.ru',
                                          'password': '123123123'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Для подтверждения аккаунта пройди по ссылке,'
                                        ' которая отправлена вам на почту')
        # проверка на отправку email
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Ссылка для активации аккаунта')

    def test_auth_test_user(self):
        response = self.client.post('/api/v1/login/auth/',
                                    data={'email': 'user@mail.ru',
                                          'password': 'user@mail.ru'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Авторизация тестового юзера прошла успешно')

    def test_auth(self):
        response = self.client.post('/api/v1/login/auth/',
                                    data={'email': 'user1@mail.ru',
                                          'password': 'user1@mail.ru'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Вход выполнен успешно')

    def test_register_try(self):
        response = self.client.post('/api/v1/login/register_try/',
                                    data={'email': 'user1@mail.ru'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post('/api/v1/login/register_try/',
                                    data={'email': 'user2@mail.ru'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Для подтверждения аккаунта пройди по ссылке,'
                                        ' которая отправлена вам на почту')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Ссылка для активации аккаунта')

    def test_reset_password(self):
        response = self.client.post('/api/v1/login/reset_password/',
                                    data={'email': 'user1@mail.ru'},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Для сброса пароля пройдите по ссылке,'
                                        ' которая отправлена вам на почту')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Ссылка для сброса пароля')

    def test_logout(self):
        # авторизация перед выходом
        self.client.login(email='user1@mail.ru',
                          password='user1@mail.ru')

        response = self.client.post('/api/v1/login/logout/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Выход из аккаунта выполнен успешно')

    def test_delete_account(self):
        self.client.login(email='user1@mail.ru',
                          password='user1@mail.ru')

        response = self.client.delete('/api/v1/login/delete/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Аккаунт удален успешно')
