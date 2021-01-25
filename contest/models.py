from django.db import models
from django.utils.timezone import now

from user.models import User
from datetime import datetime
from config.const import CONTEST_PHASE, CONTEST_LEVEL


class Contest(models.Model):
    name = models.CharField(max_length=100)  # Name of the contest
    rule = models.CharField(max_length=100, choices=[('ICPC', 'ICPC'),
                                                     ('IOI', 'IOI')])  # ICPC, IOI styles
    start_time = models.DateTimeField()  # Start date and time of the contest
    end_time = models.DateTimeField()  # End time of the contest
    #  unix_time = models.IntegerField(default=start_time.timestamp())
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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
        return (self.end_time - self.start_time).total_seconds()

    @property
    def before_contest(self):
        return (self.start_time - now()).total_seconds()

    @property
    def before_finish(self):
        return (self.end_time - now()).total_seconds()

    @property
    def set_title(self):
        return now().strftime('%B') + ' ' + self.level.title() + ' ' + 'Contest'


class ContestRating(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    point = models.IntegerField(default=0)  # Total point for the contest
    penalty = models.IntegerField(default=0)  # Total time for submissions
    rating_change = models.IntegerField(
        default=0)  # Change of rating of th user by the contest. Evaluated by some algorithm

    class Meta:
        unique_together = ('contest', 'user',)  # A user has single rating in one contest
        ordering = ['point', '-penalty']
        db_table = 'contest_rating'
