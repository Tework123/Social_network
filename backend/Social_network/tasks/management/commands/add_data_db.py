import datetime
import os
import random
from django.contrib.auth.models import User, Permission, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker

from account.models import CustomUser, Work, Education
from album.models import Album, Photo
from chat.models import Chat, Message, Relationship
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     info_for_help = ' Впишите цифры в таком порядке:'
    #     'Пользователи, фото в альбомах, чаты, диалоги, сообщения'
    #
    #     parser.add_argument('count_users', type=int,
    #                         help='Сколько нужно пользователей?' + info_for_help)
    #     parser.add_argument('count_questions', type=int,
    #                         help='Сколько нужно вопросов?' + info_for_help)
    #     parser.add_argument('count_answers', type=int,
    #                         help='Сколько нужно ответов?' + info_for_help)
    #     parser.add_argument('count_users_answers', type=int,
    #                         help='Сколько нужно ответов пользователей?' + info_for_help)

    def handle(self, *args, **kwargs):
        fake = Faker("ru_RU")
        # count_users = kwargs['count_users']
        # count_questions = kwargs['count_questions']
        # count_answers = kwargs['count_answers']
        # count_users_answers = kwargs['count_users_answers']

        # добавляем админа
        admin = CustomUser.objects.create_superuser(email='admin@mail.ru',
                                                    password='admin')

        # добавляем пользователей
        for i in range(1, 4):
            name = fake.name()
            name_join = name.replace(' ', '')
            city = fake.city()
            job = fake.job()
            if i == 1:
                name_join = 'user'

            user = CustomUser.objects.create_user(email=name_join + '@mail.ru',
                                                  password=name_join + '@mail.ru',
                                                  is_active=True,
                                                  first_name=name.split(' ')[0],
                                                  last_name=name.split(' ')[1],
                                                  # phone=fake.phone_number(),
                                                  city=city,
                                                  about_me=job,

                                                  # avatar=SimpleUploadedFile(avatar_absolute_path, new_image.read()),
                                                  date_of_birth=timezone.now()
                                                                - relativedelta(years=35),
                                                  interest=fake.text()
                                                  )
            # дополнить поля
            for _ in range(2):
                Work.objects.create(name=fake.company(), city=city,
                                    status='работник', date_start=timezone.now(),
                                    date_stop=timezone.now(), user=user)

            for _ in range(2):
                Education.objects.create(name=fake.company(), city=city,
                                         date_graduation=timezone.now(), status='выпускник',
                                         level='средний',
                                         user=user)

            avatar_absolute_path = os.path.abspath(f"Social_network/media/photos/animal{i}.jpg")

            # создаем альбом для фото профиля и фото профиля
            album_avatar = Album.objects.create(name='Фото профиля', user=user, avatar_album=True)
            with open(avatar_absolute_path, 'rb') as new_image:
                photo = SimpleUploadedFile(avatar_absolute_path, new_image.read())
                avatar = Photo.objects.create(image=photo, text=fake.text(), user=user)

                album_avatar.photo.add(avatar)

            # создаем альбом
            album = Album.objects.create(name=fake.color_name() + ' альбом', user=user)
            for _ in range(2):
                random_digit = random.randrange(1, 14)
                album_photo_absolute_path = os.path.abspath(
                    f"Social_network/media/photos/nature{random_digit}.jpg")

                with open(album_photo_absolute_path, 'rb') as new_image:
                    photo = SimpleUploadedFile(album_photo_absolute_path, new_image.read())
                    photo = Photo.objects.create(image=photo, text=fake.text(), user=user)
                    album.photo.add(photo)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Пользователи добавлены'))
        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Альбомы добавлены'))
        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Фото добавлены'))

        users = CustomUser.objects.all()
        photos = Photo.objects.all()

        for _ in range(3):
            chat_name = fake.color_name() + ' чат'
            chat = Chat.objects.create(name=chat_name, open_or_close=True)

            # добавляем в чаты пользователей
            for user in users:
                chat.user.add(user)
                for _ in range(3):
                    # добавляем в чаты сообщения от этих пользователей
                    message = Message.objects.create(text=fake.text(),
                                                     user=user,
                                                     chat_id=chat.pk,
                                                     date_create=timezone.now(),
                                                     mock=False)
                    digit = random.randrange(0, len(photos))

                    photos = random.choices(population=[photos[:digit], photos[digit], []],
                                            weights=[0.1, 0.2, 0.7], k=1)

                    # добавляем к этим сообщениям фото
                    if photos[0]:
                        for photo in photos:
                            message.photo.add(photo)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Сообщения добавлены в чаты'))

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

            digit = random.randrange(0, len(photos))

            photos = random.choices(population=[photos[:digit], photos[digit], []],
                                    weights=[0.1, 0.2, 0.7], k=1)

            # добавляем к этим сообщениям фото
            if photos[0]:
                for photo in photos:
                    message.photo.add(photo)

        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Диалоги добавлены'))
        self.stdout.write(self.style.HTTP_NOT_MODIFIED('Сообщения добавлены в диалоги'))

        self.stdout.write(self.style.SUCCESS('База данных успешно создана!'))

# надо еще поработать над рандомом, количество людей и тд, потом поделить на разные модули
