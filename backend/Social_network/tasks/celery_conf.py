import os
from datetime import timedelta

# if os.environ.get('ENV') == 'production':
# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
# CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")

# CELERY_BROKER_URL = 'amqp://localhost'
# CELERY_RESULT_BACKEND = 'amqp://localhost'

# CELERY_BROKER_URL = 'amqp://myuser:mypassword@127.0.0.1:5672/myvhost'
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672/'

result_backend = 'rpc://'

# CELERY_RESULT_BACKEND = 'amqp://myuser:mypassword@localhost:5672/myvhost'

# else:
#     # BROKER_URL = 'redis://localhost:6379'
#     CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://localhost:6379/")
#     CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://localhost:6379/")

# CELERY_ACCEPT_CONTENT = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
broker_connection_retry_on_startup = True

# запустить через консоль worker:
# celery -A tasks worker -l info -n hel


CELERY_TASK_ROUTES = {
    # test
    'tasks.tasks.task_1': {'queue': 'task_1', },
    'tasks.tasks.task_2': {'queue': 'task_2', },
    'tasks.tasks.test_task': {'queue': 'test_task', },

    'tasks.tasks.upload_photos': {'queue': 'photos', },
    'tasks.tasks.task_db': {'queue': 'task_db', },
    'tasks.tasks.celery_send_to_email': {'queue': 'email', },
}

imports = [
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
