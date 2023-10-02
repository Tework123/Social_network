import os
from datetime import timedelta

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")

CELERY_IMPORTS = [
    # name django_app, name folder, name file
    'tasks.tasks',

]

# # переписать на классах
# # доделать по статьям, написать для email и еще что нибудь

CELERY_BEAT_SCHEDULE = {
    "create_task": {
        "task": "tasks.tasks.create_task",
        'schedule': timedelta(seconds=9),
    },
}
