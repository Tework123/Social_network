from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('ENGINE'),
#         'NAME': 'social_network',
#         'USER': 'postgres',
#         'PASSWORD': os.environ.get('PASSWORD'),
#         'HOST': os.environ.get('HOST'),
#         'PORT': os.environ.get('PORT'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'social_network',
        'USER': 'postgres',
        'PASSWORD': 'ksflkOkas23fl9saflKdl349sLfsk1',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# python manage.py runserver --settings=quiz_api.settings.development
