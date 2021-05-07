from django.db import models


class Submission(models.Model):
    user = models.ForeignKey(to='user.User', related_name='submissions', on_delete=models.CASCADE)
    problem = models.ForeignKey(to='problem.Problem', related_name='submissions', on_delete=models.CASCADE)
    contest = models.ForeignKey(to='contest.Contest', related_name='submissions', on_delete=models.SET_NULL, null=True)
    source_code = models.TextField()
    submit_time = models.DateTimeField()
    language = models.CharField(max_length=10)
    language_name = models.CharField(max_length=50, default='')

    verdict = models.CharField(max_length=100)
    time = models.IntegerField(default=1000)  # Execution time in milliseconds
    memory = models.IntegerField(default=0)  # Memory usage in execution
    ip = models.GenericIPAddressField(null=True)  # Ip address via which code is submitted

    class Meta:
        ordering = ['-submit_time']
        db_table = 'submission'
