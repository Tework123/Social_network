import logging
import os
from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # rest
    'rest_framework',

    # debug panel
    "debug_toolbar",

    # library for phone_field
    "phonenumber_field",

    # cors
    'corsheaders',

    # swagger
    'drf_yasg',

    # whitenoise
    'whitenoise.runserver_nostatic',

    # apps
    'account.apps.AccountConfig',
    'album.apps.AlbumConfig',
    'chat.apps.ChatConfig',
    'community.apps.CommunityConfig',
    'login.apps.LoginConfig',
    'post.apps.PostConfig',
    'tasks.apps.TasksConfig'
]
AUTH_USER_MODEL = 'account.CustomUser'

# авторизация в тестах работает и без него
# AUTHENTICATION_BACKENDS = ['login.models.EmailBackend']


MIDDLEWARE = [
    # cors
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # debug panel
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    # date_last_visit
    'middleware.FilterIPMiddleware',

    # whitenoise for static files
    "whitenoise.middleware.WhiteNoiseMiddleware",

]

ROOT_URLCONF = 'Social_network.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Social_network.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get("MAIL_SERVER")
EMAIL_HOST_USER = os.environ.get("MAIL_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAIL_PASSWORD")
EMAIL_PORT = os.environ.get("MAIL_PORT")

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    # 'DATETIME_FORMAT': "%d.%m.%Y",

    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',

    ],

    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 10,
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',

]

# должно было быть для nginx swagger, но и без этого работает
# USE_X_FORWARDED_HOST = True

# maybe for swagger nginx https
# don`t work https swagger without them
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000',
                        'http://127.0.0.1:3000',
                        ]

CORS_ALLOW_ALL_ORIGINS = True
# or this:
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     'http://localhost:3030',
# ]

# for cookies
CORS_ALLOW_CREDENTIALS = True

# done mistake in console
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# # cookies
# CSRF_COOKIE_HTTPONLY = True
# SESSION_COOKIE_HTTPONLY = True
#
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 180

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = '/static/'

# whitenoise best
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/new_photos')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# sentry
env = os.environ.get('ENV')
if env == 'production':
    environment = "production",
else:
    environment = ''

sentry_sdk.init(
    dsn="https://2543d6c5f1e96587e2ab049b87d6b73a@o4505633113112576."
        "ingest.sentry.io/4506018116993024",
    traces_sample_rate=1.0,
    environment=environment,
    profiles_sample_rate=1.0,
)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#             'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt': "%d/%b/%Y %H:%M:%S"
#         },
#     },
#     'handlers': {
#         'null': {
#             'level': 'DEBUG',
#             'class': 'logging.NullHandler',
#         },
#         'logfile': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'Social_network' + "/logfile",
#             'maxBytes': 50000,
#             'backupCount': 2,
#             'formatter': 'standard',
#         },
#         'console': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'standard'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'propagate': True,
#             'level': 'WARN',
#         },
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'MYAPP': {
#             'handlers': ['console', 'logfile'],
#             'level': 'DEBUG',
#         },
#     }
# }
