from django.test import TestCase
from .models import User

import requests, json

users = User.objects.all()
print(users[0].get_)
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