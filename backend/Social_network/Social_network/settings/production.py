from .base import *
from dotenv import load_dotenv

load_dotenv()

ALLOWED_HOSTS = ['localhost']
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('ENGINE'),
        'NAME': os.environ.get('NAME'),
        'USER': 'postgres',
        'PASSWORD': os.environ.get('PASSWORD'),
        'HOST': os.environ.get('HOST'),
        'PORT': os.environ.get('PORT'),
    }
}