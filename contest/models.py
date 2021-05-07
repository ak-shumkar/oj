from django.db import models
from django.db.models import Q
from django.utils.timezone import now

from problem.models import Problem
from user.models import User
from submission.models import Submission
from datetime import datetime
from config.const import CONTEST_PHASE, CONTEST_LEVEL
import time


class Contest(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)  # Name of the contest
    rule = models.CharField(max_length=100, choices=[('ICPC', 'ICPC'),
                                                     ('IOI', 'IOI')])  # ICPC, IOI styles
    start_time = models.DateTimeField()  # Start date and time of the contest
    end_time = models.DateTimeField()  # End time of the contest
    author = models.ForeignKey(to='user.User', on_delete=models.CASCADE)
    description = models.TextField()
    level = models.CharField(default='novice',
                             max_length=100,
                             choices=CONTEST_LEVEL)

    class Meta:
        db_table = 'contest'

    @property
    def phase(self):
        if self.start_time > now():
            return 'future'
        elif self.end_time < now():
            return 'past'
        else:
            return 'ongoing'

    @property
    def contest_duration(self):
        seconds = (self.end_time - self.start_time).total_seconds()
        minute, sec = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return "%02d:%02d" % (hour, minute)

    @property
    def before_contest(self):
        return (self.start_time - now()).total_seconds()

    @property
    def before_finish(self):
        return (self.end_time - now()).total_seconds()

    @property
    def get_title(self):
        index = Contest.objects.filter(Q(level=self.level), Q(start_time__lt=self.start_time)).count()
        return f'CodeBattle {self.level.title()} Contest #{index + 1}'


def initial_verdicts():
    return {
        'A': 0,
        'B': 0,
        'C': 0,
        'D': 0,
        'E': 0,
        'F': 0,
        'G': 0,
        'H': 0,
        'I': 0,
        'J': 0,
        'K': 0,
        'L': 0,
        'M': 0,
        'N': 0
    }


class ContestRating(models.Model):
    contest = models.ForeignKey(to='contest.Contest', related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(to='user.User', related_name='ratings', on_delete=models.CASCADE)
    point = models.IntegerField(default=0)  # Total point for the contest
    penalty = models.IntegerField(default=0)  # Total time for submissions
    rating_change = models.IntegerField(
        default=0)  # Change of rating of th user by the contest. Evaluated by some algorithm
    verdicts = models.JSONField(default=initial_verdicts)
    penalties = models.JSONField(default=initial_verdicts)
    solved_count = models.SmallIntegerField(default=0)
    computed = models.BooleanField(default=False)  # whether elo was computed

    class Meta:
        unique_together = ('contest', 'user',)  # A user has single rating in one contest
        ordering = ['-solved_count', 'penalty']
        db_table = 'contest_rating'

    def total_penalty(self):
        res = 0
        for [k, v] in self.penalties.items():
            res += v

        return res
