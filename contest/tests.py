from django.test import TestCase
from pytz import utc

from user.models import User
from .models import Contest
from datetime import datetime


class ContestTest(TestCase):
    # def setUp(self) -> None:
    #     user = User.objects.create_user(
    #         username='pipiti',
    #         password='edefefcd'
    #     )
    #     user.save()
    #     self.user = user

    def test_create_contest(self):
        # print(self.user)
        # contest = Contest(
        #     name='Alien Contest',
        #     style='IOI',
        #     duration=8100,
        #     start_time=datetime(year=2020, month=12, day=17, hour=12, minute=0, second=0, microsecond=0),
        #     end_time=datetime(year=2020, month=12, day=17, hour=14, minute=0, second=0, microsecond=0),
        #     author=self.user,
        #     description='First ever contest',
        #     level='general'
        # )
        #
        # contest.save()
        # print('Successful')
        # self.assertEqual(contest.style, 'IOI')
        # self.assertEqual(contest.author.username, 'pipiti')
        print(User.objects.all().first())
# print(datetime(year=2020, month=12, day=17, hour=12, minute=0, second=0, microsecond=0))

