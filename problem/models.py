from django.db import models
from django.utils.timezone import now

from user.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from contest.models import Contest


class Problem(models.Model):
    """ Fields """
    # Id of problem in contest (alphabetical)
    _id = models.CharField(max_length=3, null=True)
    title = models.CharField(max_length=500)
    description = models.TextField()
    # difficulty in range [1, 100]
    difficulty = models.IntegerField(null=True, validators=[MaxValueValidator(100), MinValueValidator(1)])
    input_description = models.TextField()
    output_description = models.TextField()
    # in milliseconds
    time_limit = models.IntegerField()
    # in megabytes
    memory_limit = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, related_name='problems', blank=True, null=True, on_delete=models.SET_NULL)
    create_time = models.DateField(auto_now_add=True)
    source = models.TextField(null=True)
    # score of the problem in contest
    score = models.IntegerField(default=0)
    # sample input and output
    samples = models.JSONField(default=dict)

    class Meta:
        ordering = ['-create_time']
        db_table = 'problem'
        unique_together = ('_id', 'contest')

    # Methods
    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tag'


class Test(models.Model):
    problem = models.ForeignKey(Problem, related_name='tests', on_delete=models.CASCADE)
    input = models.FileField(upload_to='tests/inputs/')
    output = models.FileField(upload_to='tests/outputs/')

    class Meta:
        db_table = 'test'


