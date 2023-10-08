from .base import *

ALLOWED_HOSTS = [ '45.141.76.71', 'localhost', '127.0.0.1', '0.0.0.0', 'backend']
# ALLOWED_HOSTS = ["*"]
DEBUG = False

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)

# CSRF_COOKIE_HTTPONLY = False
# SESSION_COOKIE_HTTPONLY = False
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False

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
