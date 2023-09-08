from .base import *

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('ENGINE'),
        'NAME': 'social_network1',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT': os.environ.get('PORT'),
    }
}

# python manage.py runserver --settings=quiz_api.settings.development
