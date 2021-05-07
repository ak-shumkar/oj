from django.db.models import Q
from django.test import TestCase
from pytz import utc

from user.models import User
from .models import Contest, ContestRating
from datetime import datetime
import random

# class ContestTest(TestCase):
    # def setUp(self) -> None:
    #     user = User.objects.create_user(
    #         username='pipiti',
    #         password='edefefcd'
    #     )
    #     user.save()
    #     self.user = user

    # def test_create_contest(self):
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
        # print(User.objects.all().first())
# print(datetime(year=2020, month=12, day=17, hour=12, minute=0, second=0, microsecond=0))
def search(ratings, rating):
    r = len(ratings) - 1
    l = 0
    while l < r:
        m = (l + r) // 2
        current = ratings[m]
        # if current == rating:
        if current['solved_count'] == rating.solved_count and current['penalty'] == rating.penalty:
            print('Found')
            return m + 1
        elif current['solved_count'] > rating.solved_count:
            l = m+1
        elif current['solved_count'] < rating.solved_count:
            r = m-1

        else:
            if current['penalty'] < rating.penalty:
                l = m+1
            else:
                r = m-1

#     return l+1
# ratings = ContestRating.objects.filter(Q(contest_id=8), ~Q(penalty=0)).order_by('-solved_count', 'penalty')
# ratings_distinct = ContestRating.objects.filter(Q(contest_id=8), ~Q(penalty=0)).order_by('-solved_count', 'penalty').values('solved_count', 'penalty').distinct()
# # print(ratings_distinct)
# ratings_distinct = list(ratings_distinct)
# # print(len(ratings))
# rating = random.choice(ratings)
# # rating = ratings.last()
# print(f'Place of user {rating.user_id} is {search(ratings_distinct, rating)}')
