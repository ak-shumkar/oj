from django.db import models

from contest.models import Contest
from problem.models import Problem
from user.models import User


class Submission(models.Model):
    user = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, related_name='submissions', on_delete=models.SET_NULL, null=True)
    source_code = models.TextField(null=True, blank=True)
    submit_time = models.DateTimeField()
    language = models.CharField(max_length=100)

    verdict = models.CharField(max_length=100)
    time = models.IntegerField(default=1000)  # Execution time in milliseconds
    memory = models.IntegerField(default=0)  # Memory usage in execution
    ip = models.GenericIPAddressField(null=True)  # Ip address via which code is submitted

    class Meta:
        ordering = ['-submit_time']
        db_table = 'submission'
