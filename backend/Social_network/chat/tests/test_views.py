import os
from faker import Faker
from django.test import TestCase
from rest_framework import status
from account.models import CustomUser
from album.models import Album, Photo
from django.core.files.uploadedfile import SimpleUploadedFile

from chat.models import Chat, Message

fake = Faker()
absolute_path = os.path.abspath("Social_network/media/photos/shrek.jpg")


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
                new_photo = Photo.objects.create(image=photo, text=photo_text, user=test_user)

        users = []
        users.insert(0, test_user)

        for _ in range(3):
            email = fake.name() + '@mail.ru'
            user = CustomUser.objects.create_user(email=email,
                                                  password=email, is_active=True)
            users.append(user)

        photos = Photo.objects.all()

        for _ in range(3):
            chat_name = fake.name()
            chat = Chat.objects.create(name=chat_name, open_or_close=True)

            # добавляем в чаты пользователей
            for user in users:
                chat.user.add(user)

                # добавляем в чаты сообщения от этих пользователей
                message = Message.objects.create(text=fake.text(),
                                                 user=user,
                                                 chat_id=chat.pk,
                                                 mock=False)

                # добавляем к этим сообщениям фото
                for photo in photos:
                    message.photo.add(photo)

    @staticmethod
    def get_user() -> CustomUser:
        """Возвращает тестового пользователя"""

        user = CustomUser.objects.get(email='user@mail.ru')
        return user

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
                                          'user': [2, 3, 4]},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Беседа создана успешно')

        response = self.client.get('/api/v1/chat/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_chat_edit(self):
        response = self.client.put('/api/v1/chat/1/',
                                   data={'name': 'my_chat1',
                                         'open_or_close': False,
                                         'user': [2, 3]},
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

    # мок и сообщения нужно в одном тесте вместе проверять, они связаны сильно
    def test_messages_message_mock_chat(self):
        # создаем mock сообщения (неотправленное)
        response = self.client.get('/api/v1/chat/messages_mock/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 32)

        # прикрепляем к нему фото
        response = self.client.put('/api/v1/chat/messages_mock/1/',
                                   data={'name': 'my_chat1',
                                         'open_or_close': False,
                                         'user': [2, 3]},
                                   content_type="application/json")

        # отправляем сообщение в чат
        response = self.client.put('/api/v1/chat/messages/1/',
                                   data={'name': 'my_chat1',
                                         'open_or_close': False,
                                         'user': [2, 3]},
                                   content_type="application/json")

        # get для вывода всех сообщений чата(считаем новое количество)
        response = self.client.get('/api/v1/chat/messages/1/')
        # под такое пиво можно и гитхаб тесты подключить

    def test_messages_chat(self):
        response = self.client.get('/api/v1/chat/messages/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 32)

    def test_dialog(self):
        pass

    def test_dialog_create(self):
        pass

    def test_dialog_edit(self):
        pass

    def test_messages_dialog(self):
        pass

    def test_messages_mock_dialog(self):
        pass

    def test_message(self):
        pass

    def test_clear_files(self):
        photos = Photo.objects.all()
        for photo in photos:
            photo.image.delete(save=True)
            photo.delete()
