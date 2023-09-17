import time

from celery import shared_task
from celery.utils.log import logger


@shared_task
def create_task(task_type=1):
    logger.info("Я иду по выжженной земле")

    time.sleep(task_type * 3)
    return True
