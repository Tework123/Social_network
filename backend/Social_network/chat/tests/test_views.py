import os
from faker import Faker
from django.test import TestCase
from rest_framework import status
from account.models import CustomUser
from album.models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile

from chat.models import Chat, Message, Relationship

fake = Faker()
absolute_path = os.path.abspath("Social_network/media/base_photos/shrek.jpg")


class ChatViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """Заполняет данными базу"""

        test_user = CustomUser.objects.create_user(email='user@mail.ru',
                                                   password='user@mail.ru', is_active=True)

        # добавляем фото для прикрепления к сообщениям
        for _ in range(3):
            photo_text = fake.name()
            with open(absolute_path, 'rb') as new_image:
                photo = SimpleUploadedFile(absolute_path, new_image.read())
                Photo.objects.create(image=photo, text=photo_text, user=test_user)

        for _ in range(3):
            email = fake.name() + '@mail.ru'
            CustomUser.objects.create_user(email=email,
                                           password=email, is_active=True)

        users = CustomUser.objects.all()
        photos = Photo.objects.all()

        for _ in range(3):
            chat_name = fake.name()
            chat = Chat.objects.create(name=chat_name, open_or_close=True)

            # добавляем в чаты пользователей
            for user in users:
                chat.user.add(user)
                for _ in range(3):
                    # добавляем в чаты сообщения от этих пользователей
                    message = Message.objects.create(text=fake.text(),
                                                     user=user,
                                                     chat_id=chat.pk,
                                                     mock=False)

                    # добавляем к этим сообщениям фото
                    for photo in photos:
                        message.photo.add(photo)

        # создаем диалоги
        relationship = Relationship.objects.create(user_1=users[0],
                                                   user_2_id=users[1].id,
                                                   status='friend')
        Relationship.objects.create(user_1=users[2],
                                    user_2_id=users[3].id,
                                    status='friend')
        # добавляем в диалог сообщения
        for _ in range(3):
            message = Message.objects.create(text=fake.text(),
                                             user=users[0],
                                             relationship_id=relationship.id,
                                             mock=False)
            # добавляем к этим сообщениям фото
            for photo in photos:
                message.photo.add(photo)

    @staticmethod
    def get_user() -> CustomUser:
        """Возвращает тестового пользователя"""

        user = CustomUser.objects.get(email='user@mail.ru')
        return user

    @staticmethod
    def get_users_id() -> list[CustomUser]:
        users = CustomUser.objects.all().values_list('id', flat=True)
        return users

    @staticmethod
    def get_users() -> list[CustomUser]:
        users = CustomUser.objects.all()
        return users

    @staticmethod
    def get_photos() -> list[Photo]:
        photos = Photo.objects.all().values_list('id', flat=True)
        return photos

    def setUp(self) -> None:
        """Авторизует пользователя перед каждым тестом"""

        self.client.login(email='user@mail.ru',
                          password='user@mail.ru')

    def test_chat(self):
        response = self.client.get('/api/v1/chat/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_chat_create(self):

        response = self.client.post('/api/v1/chat/',
                                    data={'name': 'my_chat',
                                          'open_or_close': True,
                                          'user': list(self.get_users_id())},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Беседа создана успешно')

        response = self.client.get('/api/v1/chat/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_chat_edit(self):

        response = self.client.patch('/api/v1/chat/1/',
                                     data={'name': 'my_chat1',
                                           'open_or_close': False,
                                           'user': list(self.get_users_id()[1:3])},
                                     content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Беседа успешно изменена')

        chat = Chat.objects.get(pk=1)
        self.assertEqual(len(chat.user.all()), 2)

    def test_chat_delete(self):
        response = self.client.delete('/api/v1/chat/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Беседа успешно удалена')

        response = self.client.get('/api/v1/chat/')
        self.assertEqual(len(response.data), 2)

    def test_messages_chat(self):
        response = self.client.get('/api/v1/chat/messages/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 12)

    # мок и сообщения нужно в одном тесте вместе проверять, они связаны сильно
    def test_messages_message_mock_chat(self):
        # создаем mock сообщения (неотправленное)
        response = self.client.get('/api/v1/chat/messages_mock/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # прикрепляем к нему фото
        response = self.client.put('/api/v1/chat/messages_mock/1/',
                                   data={'photo': list(self.get_photos())},
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Фото добавлены к сообщению')

        # отправляем сообщение в чат
        response = self.client.put('/api/v1/chat/messages/1/',
                                   data={'text': fake.text()},
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Сообщение добавлено в чат')

        # get для вывода всех сообщений чата(считаем новое количество)
        response = self.client.get('/api/v1/chat/messages/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 13)

    # relationship
    def test_dialog(self):
        response = self.client.get('/api/v1/chat/dialogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_dialog_create_already_exist(self):

        response = self.client.post('/api/v1/chat/dialogs/',
                                    data={'status': 'friend',
                                          'user_2': self.get_users()[0].id},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'Этот пользователь уже связан с тобой')

    def test_dialog_create(self):

        response = self.client.post('/api/v1/chat/dialogs/',
                                    data={'status': 'friend',
                                          'user_2': self.get_users()[2].id},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Отношения с пользователем установлены')

        response = self.client.get('/api/v1/chat/dialogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_dialog_edit(self):
        response = self.client.patch('/api/v1/chat/dialogs/1/',
                                     data={'status': 'enemy'
                                           },
                                     content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Отношения с пользователем изменены')

    def test_dialog_delete(self):
        response = self.client.delete('/api/v1/chat/dialogs/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Отношения успешно удалены')

        response = self.client.get('/api/v1/chat/dialogs/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get('/api/v1/chat/dialogs/')
        self.assertEqual(len(response.data), 0)

    def test_messages_dialog(self):
        response = self.client.get('/api/v1/chat/dialogs/messages/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    # мок и сообщения нужно в одном тесте вместе проверять, они связаны сильно
    def test_messages_message_mock_dialog(self):
        # создаем mock сообщения (неотправленное)
        response = self.client.get('/api/v1/chat/dialogs/messages_mock/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # прикрепляем к нему фото
        response = self.client.put('/api/v1/chat/dialogs/messages_mock/1/',
                                   data={'photo': list(self.get_photos())},
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Фото добавлены к сообщению')

        # отправляем сообщение в диалог
        response = self.client.put('/api/v1/chat/dialogs/messages/1/',
                                   data={'text': fake.text()},
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Сообщение добавлено в отношение')

        # get для вывода всех сообщений диалога(считаем новое количество)
        response = self.client.get('/api/v1/chat/dialogs/messages/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    # messages
    def test_message(self):

        response = self.client.patch('/api/v1/chat/message/1/',
                                     data={'text': fake.text(),
                                           'photo': list(self.get_photos())},
                                     content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Сообщение изменено')

        response = self.client.get('/api/v1/chat/message/1/')
        self.assertEqual(len(response.data['photo']), 3)

    def test_message_delete(self):
        response = self.client.delete('/api/v1/chat/message/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Сообщение удалено')

        response = self.client.get('/api/v1/chat/message/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get('/api/v1/chat/messages/1/')
        self.assertEqual(len(response.data), 11)

    @staticmethod
    def test_clear_files():
        photos = Photo.objects.all()
        for photo in photos:
            photo.image.delete(save=True)
            photo.delete()
