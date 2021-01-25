from django.test import TestCase
from .models import Submission

s = Submission.objects.latest('id')
print(s.problem_id)
