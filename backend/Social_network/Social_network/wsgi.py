"""
WSGI config for Social_network project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# возможно здесь нужно тоже поменять, либо этот файл только для продакшена используется
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Social_network.settings.production')

application = get_wsgi_application()
