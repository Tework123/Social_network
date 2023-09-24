from django.urls import reverse
from faker import Faker
from django.test import TestCase
from rest_framework.test import APITestCase

from account.models import CustomUser, Work, Education

fake = Faker()


class AccountViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = CustomUser.objects.create_user(email='user@mail.ru',
                                              password='user@mail.ru', is_active=True)

        for i in range(3):
            work_name = fake.company()
            Work.objects.create(name=work_name, user=user)

        for i in range(2):
            education_name = fake.company()
            Education.objects.create(name=education_name, user=user)

    def setUp(self) -> None:
        self.client.login(email='user@mail.ru',
                          password='user@mail.ru')

    def get_user(self):
        user = CustomUser.objects.get(email='user@mail.ru')
        return user

    def test_account(self):
        response = self.client.get('/api/v1/account/im/')
        self.assertEqual(response.status_code, 200)

    def test_account_work(self):
        response = self.client.get('/api/v1/account/edit/work/')
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 200)

    def test_account_work_create(self):
        response = self.client.post('/api/v1/account/edit/work/',
                                    data={'name': 'hello_dodik',
                                          'city': 'city',
                                          'status': '',
                                          'date_start': None,
                                          'date_stop': None,
                                          'user': self.get_user().id},
                                    content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 200)

    def test_account_education_create(self):
        response = self.client.get('/api/v1/account/edit/work/')
        self.assertEqual(response.status_code, 200)

    def test_account_education(self):
        response = self.client.get('/api/v1/account/edit/education/')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

# как же в падлу писать тесты...................
# нужно оттестировать все запросы в аккаунте, потом переходить на альбом...
# только True будем? Наверное
# в чате надо проверить блокировку в чужим чатах и сообщениях
# надо кончить это дело с тестами...
