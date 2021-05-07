from django.test import TestCase

from submission.models import Submission
from .models import Test, Problem, Editorial
from django.utils.timezone import now
from termcolor import colored


print(colored('LOCATION: problem.tests start ...', 'magenta'))


def get_verdicts():
    try:
        result = dict()
        problems = Problem.objects.filter(contest_id=2)
        for problem in problems:
            try:
                submissions = Submission.objects.filter(contest_id=2, problem=problem)
            except Submission.DoesNotExist:
                result[problem._id] = ''
            else:
                if submissions:
                    result[problem._id] = submissions.order_by('verdict').first().verdict
                else:
                    result[problem._id] = ''

    except Exception as e:
        print(e)
        return {}
    else:
        return result


# print(get_verdicts())
problems = Problem.objects.all()
for problem in problems:
    Editorial.objects.create(problem=problem)

print(colored('LOCATION: problem.tests end ...', 'yellow'))