import os
from django.contrib.auth import authenticate, login
from dotenv import load_dotenv
from login.email import send_to_email
from tasks.tasks import celery_send_to_email

from account.models import CustomUser


def create_test_user(email, password, request):
    try:
        user = CustomUser.objects.get(email=email)
    except:
        user = CustomUser.objects.create_user(email=email,
                                              password=password,
                                              is_active=True)
    user = authenticate(email=user.email,
                        password=password)
    login(request, user)


load_dotenv()
env = os.environ.get('ENV')


def send_email_env(email, mail_subject, template_name):
    if env == 'production':
        # отправка на email celery task
        celery_send_to_email.delay(email=email,
                                   mail_subject=mail_subject,
                                   template_name=template_name)
    else:
        send_to_email(email=email, mail_subject=mail_subject,
                      template_name=template_name)
