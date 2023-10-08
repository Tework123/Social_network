# Social_network

## Использованные технологии:

### Frontend(писал DenisFrol7):

- React

### Backend(писал Tework123):

- Django Веб-фреймворк
- Django REST FRAMEWORK Для написания api
- drf_yasg Open-api документация

### Веб-приложение развернуто на VPS с помощью docker(из ветки main).

### Docker-conteiners:

- frontend(nginx+react-app)
- backend(django(qunicorn))
- db(postgres)
- pgbackups
- certbot
- rabbitmq(celery, cash)

## Функциональность сайта:

- авторизация пользователей по ссылке с почты
- профиль пользователя
- чат
- группы
- посты

Also:

- unittest api

## Схема базы данных:

![image](https://github.com/Tework123/Bakery/assets/115368408/1b9c6443-78dc-4302-adc7-824a72329320)

## Документация open-api(swagger):

https://documenter.getpostman.com/view/25883857/2s946k6B7S

![image](https://github.com/Tework123/Bakery/assets/115368408/08d2515f-d409-42e5-b2bc-2e6837c54434)

## Установка:

Создаем новую папку, создаем виртуальное окружение, активируем его.

Подключаем git к папке:

    git init 
    git clone https://github.com/Tework123/Social_network.git

### Установка backend:

Заходим в папку с приложением django:

    cd backend
    cd Social_network

Устанавливаем зависимости:

    pip install -r requirements.txt

Создаем .env файл в папке с docker-compose.

Заполняем .env файл примерно так:

    SQLALCHEMY_DATABASE_URI_POSTGRES = 'postgresql://postgres:password@localhost:5432/name_db'
    SQLALCHEMY_DATABASE_URI_POSTGRES_prod = 'postgresql://postgres:password@db:5432/name_db'
    SQLALCHEMY_DATABASE_URI_POSTGRES_TEST = 'postgresql://postgres:password@localhost:5432/name_db_test'
    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'password'
    POSTGRES_DB = 'name_db'
    
    SECRET_KEY = 'asldkk12kelakfjafkj23jijraijfi23jappweovm1'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'myemail@gmail.com'
    MAIL_PASSWORD = 'sadasdkmvxvvqlwl'
    ADMINS = 'myemail@gmail.com'
    ADMIN_LOGIN = 'admin@admin.com'
    ADMIN_PASSWORD = 'admin'
    REDIS_URL_LOCAL = 'redis://127.0.0.1:6379'
    REDIS_URL_server = 'redis://redis:6379'
    REDIS_PASSWORD = 'mzxcvm213zmvdsf@k3ll1'

Локально поднимаем postgres, redis.

### Установка frontend:

- some code

В папке с django приложением запускаем локальный сервер:

    python manage.py runserver

### Services:

requirements:

    pip install -r requirements.txt

tests:

    python -m flake8

test coverage:

    coverage run manage.py test
    python -m coverage report

flake8:

    python -m flake8

