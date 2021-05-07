from django.core import mail
from django.test import TestCase
from .models import User

import requests, json, random

# with open('notebook/tokens.txt', 'a+') as f:
#     for user in users[:1]:
#         try:
#             if user.get('username') != 'kalandar':
#                 r = requests.post('http://127.0.0.1:8000/api/account/login/',
#                                   data={'username': user.get('username'),
#                                         'password': user.get('password'),
#                                         }
#                                   )
#
#                 print(r.status_code, r.json())
#         except Exception as e:
#             print(e)

# from django.conf import settings

# print(settings.EMAIL_HOST)
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.conf import settings

from rest_framework import viewsets, permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .tokens import account_activation_token
from .models import User, Profile
from .serializers import AccountCreateSerializer, LoginSerializer, UserProfileSerializer, UserDetailSerializer


def send_email():
    # current_site = get_current_site(request)
    # mail_subject = 'Activate your account'
    # message = render_to_string('acc_active_email.html', {
    #     'user': user,
    #     'domain': settings.EMAIL_HOST,
    #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #     'token': account_activation_token.make_token(user),
    # })
    # to_email = user.email
    # email = EmailMessage(
    #     mail_subject, message, to=[to_email]
    # )
    # email.send()

    print('SENDING EMAIL')
    token = get_random_string(length=32)

    verify_link = settings.FRONTEND_URL + 'email-verify/' + token
    subject, from_email = 'Verify Your Email', 'mm.kalandar@gmail.com'
    html_content = render_to_string('verify-email.html',
                                    {'verify_link': verify_link,
                                     'base_url': settings.FRONTEND_URL,
                                     'username': 'vedo'
                                     })
    text_content = strip_tags(html_content)

    # msg = EmailMultiAlternatives(subject, text_content, 'mm.kalandar@gmail.com', ['vedoxooor@gmail.com'])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send(fail_silently=True)
    # send_mail(subject, text_content, 'mm.kalandar@gmail.com', ['vedoxooor@gmail.com'])
    r = send_mail('Hello world!', 'Hello world', 'mm.kalandar@gmail.com', ['vedoxooor@gmail.com'], fail_silently=False)
    print('response ', r)
    print('EMAIL SENT')
#
# class EmailTest(TestCase):
#     def test_send_email(self):
#         # Send message.
#         mail.send_mail('Subject here', 'Here is the message.',
#             'mm.kalandar@gmail.com', ['vedoxooor@gmail.com'],
#             fail_silently=False)
#
#
#
#
#         # Test that one message has been sent.
#         self.assertEqual(len(mail.outbox), 1)
#
#         # Verify that the subject of the first message is correct.
#         self.assertEqual(mail.outbox[0].subject, 'Subject here')


class DemoUser:
    def __init__(self):
        self.email = 'vedoxooor@gmail.com'
        self.username = 'vedoxoor'


users = User.objects.all()

for user in users:
    Profile.objects.create(user=user)




