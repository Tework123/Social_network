import os

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.generics import get_object_or_404
from account.models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)
                + six.text_type(user.is_active))


account_activation_token = TokenGenerator()


def send_to_email(email, mail_subject, template_name):
    user = get_object_or_404(CustomUser, email=email)

    env = os.environ.get('ENV')
    if env == 'production':
        link = 'https'
        domain = 'tework123.store'
    else:
        link = 'http'
        domain = '127.0.0.1:8000'

    message = render_to_string(template_name, {
        'user': user,
        'link': link,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })

    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )

    email.send()
