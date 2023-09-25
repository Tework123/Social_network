import os
from faker import Faker
from django.test import TestCase
from rest_framework import status
from account.models import CustomUser
from album.models import Album, Photo
from django.core.files.uploadedfile import SimpleUploadedFile

fake = Faker()
absolute_path = os.path.abspath("Social_network/media/photos/shrek.jpg")


class AlbumViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """Заполняет данными базу"""

        user = CustomUser.objects.create_user(email='user@mail.ru',
                                              password='user@mail.ru', is_active=True)

        for i in range(3):
            album_name = fake.name()
            Album.objects.create(name=album_name, user=user)

        first_album = Album.objects.get(pk=1)

        # Загружаем фото и цепляем их к альбому
        for i in range(2):
            photo_text = fake.name()
            with open(absolute_path, 'rb') as new_image:
                photo = SimpleUploadedFile(absolute_path, new_image.read())
                new_photo = Photo.objects.create(image=photo, text=photo_text, user=user)
                first_album.photo.add(new_photo)

    @staticmethod
    def get_user() -> CustomUser:
        """Возвращает тестового пользователя"""

        user = CustomUser.objects.get(email='user@mail.ru')
        return user

    def setUp(self) -> None:
        """Авторизует пользователя перед каждым тестом"""

        self.client.login(email='user@mail.ru',
                          password='user@mail.ru')

    def test_album(self):
        response = self.client.get('/api/v1/album/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_album_create(self):
        response = self.client.post('/api/v1/album/',
                                    data={'name': 'first_album',
                                          'user': self.get_user().id},
                                    content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, 'Альбом успешно добавлен')

    def test_album_edit(self):
        response = self.client.put('/api/v1/album/1/',
                                   data={'name': 'help_album'
                                         },
                                   content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Альбом успешно изменен')

    def test_album_delete(self):
        response = self.client.delete('/api/v1/album/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/v1/album/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get('/api/v1/album/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_photo(self):
        response = self.client.get('/api/v1/album/photos/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_photo_create(self):

        # возможно пригодится для видео и файлов
        # photo = SimpleUploadedFile(absolute_path, b"file_content", content_type="image/jpeg")
        #
        # for i in range(2):
        #     photo_text = fake.name()
        #
        #     response = self.client.post('/api/v1/album/photos/1/',
        #                                 data={'image': photo,
        #                                       'text': photo_text,
        #                                       'user': self.get_user().id
        #                                       }, )
        #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #     self.assertEqual(response.data, 2)
        for i in range(2):
            with open(absolute_path, 'rb') as new_image:
                photo = SimpleUploadedFile(absolute_path, new_image.read())
                photo_text = fake.name()

                response = self.client.post('/api/v1/album/photos/1/',
                                            data={'image': photo,
                                                  'text': photo_text,
                                                  'user': self.get_user().id
                                                  }, )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data, 'Фото успешно добавлено')

    def test_photo_edit(self):
        pass
        # доделать тесты здесь и в чате...

    def test_photo_delete(self):
        pass
