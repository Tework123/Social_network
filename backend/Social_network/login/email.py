from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.generics import get_object_or_404

from account.models import CustomUser
from login.utils import account_activation_token


def send_to_email(email, mail_subject, template_name):
    user = get_object_or_404(CustomUser, email=email)

    message = render_to_string(template_name, {
        'user': user,

        # нужно сделать domain меняющимся, сервер или локальная машина
        # в темплайте надо будет еще изменить http на https
        'domain': '127.0.0.1:3000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )

    email.send()
