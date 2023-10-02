import time

from celery import shared_task
from celery.utils.log import logger

from login.email import send_to_email


@shared_task
def create_task(task_type=1):
    logger.info("Я иду по выжженной земле")

    time.sleep(task_type * 3)
    return True


@shared_task()
def celery_send_to_email(email, mail_subject, template_name):
    send_to_email(email, mail_subject, template_name)
    logger.info(f"Отправил сообщение на email: {email}")
