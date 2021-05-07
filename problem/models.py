from django.db import models

from user.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Problem(models.Model):
    """
    pid: Alphabetical is od the problem in contest
    difficulty: Difficulty between 1 and 100, inclusive.
    time_limit: Time constraint in milliseconds
    memory_limit: Memory constraint in megabytes
    score: Score in contest
    samples: Sample input and output
    """
    pid = models.CharField(max_length=3, null=True)
    title = models.CharField(max_length=256)
    description = models.TextField()
    difficulty = models.IntegerField(null=True, validators=[MaxValueValidator(100), MinValueValidator(1)])
    input_description = models.TextField()
    output_description = models.TextField()
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    author = models.ForeignKey(to='user.User', related_name='problems', on_delete=models.SET_NULL, null=True)
    contest = models.ForeignKey(to='contest.Contest', related_name='problems', blank=True, null=True,
                                on_delete=models.SET_NULL)
    create_time = models.DateField(auto_now_add=True)
    source = models.TextField(null=True)
    score = models.IntegerField(default=0)
    samples = models.JSONField(default=dict)
    clarification = models.TextField(null=True)

    class Meta:
        ordering = ['-create_time']
        db_table = 'problem'
        unique_together = ('pid', 'contest')

    def __str__(self):
        return f"{self.pid} {self.title}"


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tag'


class Editorial(models.Model):

    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    en = models.TextField(default='No editorial')
    ru = models.TextField(default='No editorial')
    kg = models.TextField(default='No editorial')

    class Meta:
        db_table = 'editorial'


class Test(models.Model):
    problem = models.ForeignKey(to='problem.Problem', related_name='tests', on_delete=models.CASCADE)
    input = models.FileField(upload_to='tests/inputs/')
    output = models.FileField(upload_to='tests/outputs/')

    class Meta:
        db_table = 'test'
