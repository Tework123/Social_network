import time

from celery import shared_task
from celery.utils.log import logger


# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
#
# from login.utils import account_activation_token


@shared_task
def create_task(task_type=1):
    logger.info("Я иду по выжженной земле")

    time.sleep(task_type * 3)
    return True

#
# @shared_task
# def send_to_email(user, mail_subject, template_name):
#     message = render_to_string(template_name, {
#         'user': user,
#
#         # нужно сделать domain меняющимся, сервер или локальная машина
#         # в темплайте надо будет еще изменить http на https
#         'domain': '127.0.0.1:3000',
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#     })
#
#     email = EmailMessage(
#         mail_subject, message, to=[user.email]
#     )
#
#     email.send()
