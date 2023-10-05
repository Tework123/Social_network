import time

import requests
from celery import shared_task
from celery.utils.log import logger

from login.email import send_to_email
from post.models import Post


@shared_task
def celery_send_to_email(email, mail_subject, template_name):
    send_to_email(email, mail_subject, template_name)
    logger.info(f"Отправил сообщение на email: {email}")


@shared_task
def upload_photos():
    logger.info(f"Грузим фоточки по тихому")
    time.sleep(20)


@shared_task
def task_db(job_params):
    logger.info(f"Пытаюсь изменить пост")
    post = Post.objects.get(pk=job_params['id'])
    post.text = 'i am win'
    post.save()
    time.sleep(5)


# не работает асинхронно, так как view ждет результата
# @shared_task
# def task_db(url):
#     logger.info("Делаю запрос на внешний апи")
#     r = requests.get(url=url)
#     time.sleep(10)
#     return r.json()

# получить результат в view:
# res = task_db.delay(url=url)
# res = res.get()

@shared_task
def task_1(task_type=1):
    logger.info("Я иду по выжженной земле")

    time.sleep(task_type * 3)
    return True


@shared_task
def task_2(task_type=1):
    logger.info("Прошу помощи, кролик убегает!")

    time.sleep(task_type * 3)
    return True


@shared_task
def test_task(url):
    logger.info("Поймал!")
    r = requests.get(url=url)
    time.sleep(1)
    return r.json()
