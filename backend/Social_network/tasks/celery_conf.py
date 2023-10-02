import os
from datetime import timedelta

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")

CELERY_TASK_ROUTES = {
    # test
    'tasks.tasks.task_1': {'queue': 'task_1', },
    'tasks.tasks.task_2': {'queue': 'task_2', },

    'tasks.tasks.upload_photos': {'queue': 'photos', },
    'tasks.tasks.task_db': {'queue': 'task_db', },
    'tasks.tasks.celery_send_to_email': {'queue': 'email', },
}

CELERY_IMPORTS = [
    # name django_app, name folder, name file
    'tasks.tasks',

]

# отсылка статистики на почту админу?
# генерация рандомных сообщений в чат?
CELERY_BEAT_SCHEDULE = {
    "task_1": {
        "task": "tasks.tasks.task_1",
        'schedule': timedelta(seconds=9),
    },
    "task_2": {
        "task": "tasks.tasks.task_2",
        'schedule': timedelta(seconds=9),
    },
}
