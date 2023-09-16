from .base import *

# ALLOWED_HOSTS = ['198.211.99.20', 'localhost', '127.0.0.1', '0.0.0.0', 'backend']
ALLOWED_HOSTS = ["*"]
DEBUG = True

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)


DATABASES = {
    'default': {
        "ENGINE": os.environ.get("ENGINE"),
        "NAME": os.environ.get("NAME"),
        "USER": os.environ.get("USER"),
        "PASSWORD": os.environ.get("PASSWORD"),
        "HOST": os.environ.get("PROD_HOST"),
        "PORT": os.environ.get("PORT"),
    }
}
