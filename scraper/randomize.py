from termcolor import colored
from django.db.models import F
from user.models import User
from contest.models import Contest, ContestRating
from problem.models import Problem
from submission.models import Submission
import random
from datetime import datetime
import pytz


class Randomize:
    def __init__(self):
        self.users = User.objects.all()
        self.contests = Contest.objects.all()
        self.problems = Problem.objects.all()
        self.user = None
        self.problem = None
        self.contest = None
        self.rating = None
        self.submission = None

    def update_rating(self):
        if self.rating:
            problem_id = self.problem.pid
            if self.rating.verdicts[problem_id] != 1 and self.submission.verdict == 'Accepted':
                self.rating.solved_count += 1
                self.rating.verdicts[problem_id] = 1
                self.rating.penalties[problem_id] += (self.submission.submit_time - self.contest.start_time).total_seconds() // 60
                self.rating.penalty = F('penalty') + int((self.submission.submit_time - self.contest.start_time).total_seconds() // 60)

            elif self.rating.verdicts[problem_id] != 1 and self.submission.verdict != 'Accepted':
                self.rating.verdicts[problem_id] = -1
                self.rating.penalties[problem_id] += 10
                self.rating.penalty = F('penalty') + 10
            else:
                pass

            self.rating.save()
            print(colored(f'Updated rating !', 'green', attrs=['bold']))
        else:
            print(colored(f'This is not contest submission !', 'green', attrs=['bold']))

    def random_submit(self, count=1):
        for cnt in range(count):
            try:
                self.user = random.choice(self.users)
                self.contest = self.contests.get(id=8) # random.choice(self.contests)
                self.problem = random.choice(self.problems.filter(contest=self.contest))

                try:
                    self.rating = ContestRating.objects.get(contest=self.contest, user=self.user)
                except ContestRating.DoesNotExist:
                    print('Registering ...')
                    self.rating = ContestRating.objects.create(user=self.user, contest=self.contest)

                self.submission = Submission.objects.create(
                    user=self.user,
                    contest=self.contest,
                    problem=self.problem,
                    source_code='some code',
                    verdict=random.choice(['Accepted', 'Wrong Answer', 'Time Limit Exceeded']),
                    language=random.randint(1, 79),
                    language_name=random.choice(['C++', 'Python', 'Java']),
                    submit_time=datetime.fromtimestamp(random.randrange(self.contest.start_time.timestamp()+10,
                                                                        self.contest.end_time.timestamp()), tz=pytz.utc)
                )
                self.update_rating()
            except Exception as e:
                print(e)
