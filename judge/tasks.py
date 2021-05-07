from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import F, Q

from judge.judger import Judger
from contest.models import ContestRating
from user.models import User
import math


@shared_task
def judge_task(submission_id):
    print(f'Judgment task has started on submission with id {submission_id}')
    Judger(submission_id).judge()


def compute_delta(user1, user2):
    r1 = user1.rating
    r2 = user2.rating
    probability = 1 / (1 + math.pow(10, (r2 - r1) / 400))
    return probability


def search(ratings, rating):
    right = len(ratings) - 1
    left = 0
    while left < right:
        m = (left + right) // 2
        current = ratings[m]

        if current['solved_count'] == rating.solved_count and current['penalty'] == rating.penalty:
            print('Found')
            return m + 1
        elif current['solved_count'] > rating.solved_count:
            left = m + 1
        elif current['solved_count'] < rating.solved_count:
            right = m - 1

        else:
            if current['penalty'] < rating.penalty:
                left = m + 1
            else:
                right = m - 1

    return left + 1


@shared_task
def compute_rating(user_id, contest_id):
    # print('[INFO] ', f'Rating computation has started for user {user_id} and contest {contest_id}')

    ratings = ContestRating.objects.filter(Q(contest_id=contest_id), ~Q(penalty=0)).order_by('-solved_count', 'penalty')
    target_rating = ratings.get(user_id=user_id)

    distinct_ratings = ratings.values('solved_count', 'penalty').distinct()
    distinct_ratings = list(distinct_ratings)

    total = ratings.count() + 1

    ratings = ratings.filter(~Q(user_id=0))

    place = search(distinct_ratings, target_rating)
    print(f'Place in contest {contest_id} of user {user_id} is {place}')
    actual = 2 * (total - place) / (total * (total - 1))
    expected = 0
    for rating in ratings:
        expected += compute_delta(target_rating.user, rating.user)

    expected *= 2
    expected /= total * (total - 1)
    # print(f'expected is {expected} of {target_rating.user_id} against {ratings.count()} users')
    # print(f'and actual is {actual}')
    delta = (100 * (total-1) / 2) * (actual - expected)
    print(f'total score of user {user_id} is {delta}')
    target_rating.rating_change = delta
    target_rating.save()

    # delta = 0
    # for rating in ratings:
    #     if target_rating.solved_count > rating.solved_count:
    #         win = 1.0
    #     elif target_rating.solved_count < rating.solved_count:
    #         win = 0.0
    #     else:
    #         if target_rating.penalty < rating.penalty:
    #             win = 1.0
    #         elif target_rating.penalty > rating.penalty:
    #             win = 0.0
    #         else:
    #             win = 0.5
    #
    #     delta += 100 * (win - (1 / (1 + math.pow(10, (rating.user.rating - target_rating.user.rating) / 400))))
    #
    # target_rating.rating_change = delta / (total - 1)
    # target_rating.save()
    # print(f'Another total score of user {user_id} is {  delta / (total-1)}')


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="compute_rating_changes",
    ignore_result=True
)
def elo():
    ratings = ContestRating.objects.filter(Q(computed=False), ~Q(penalty=0))
    for rating in ratings:
        user_id = rating.user_id
        contest_id = rating.contest_id
        compute_rating.delay(user_id, contest_id)
