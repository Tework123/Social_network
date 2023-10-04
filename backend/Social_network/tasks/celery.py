import os
from celery import Celery
from django.conf import settings

# if os.environ.get('ENV') == 'production':
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Social_network.settings.production')
# else:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Social_network.settings.development')


app = Celery("tasks")
app.config_from_object('tasks.celery_conf', namespace="CELERY")

app.autodiscover_tasks()
