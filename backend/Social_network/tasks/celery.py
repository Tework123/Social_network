import os
from celery import Celery

# from tasks.tasks import TestTask

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Social_network.settings.production')
app = Celery("tasks")
default_config = 'tasks.celery_conf'
app.config_from_object(default_config, namespace="CELERY")
app.autodiscover_tasks()
