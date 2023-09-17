import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Social_network.settings.production')
app = Celery("tasks")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
