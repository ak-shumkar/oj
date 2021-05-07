from django.db.models import F

from problem.models import Problem, Test
from submission.models import Submission
from contest.models import ContestRating, Contest
import requests
import time
import coloredlogs
import logging
logger = logging.getLogger(__name__)
logger = coloredlogs.install(level='INFO', logger=logger)


class Judger:
    def __init__(self, submission_id):
        self.submission = Submission.objects.get(id=submission_id)
        self.problem = Problem.objects.get(id=self.submission.problem_id)
        self.tests = Test.objects.filter(problem=self.problem)
        self.contest = None
        self.rating = None
        # ------------------
        self.test = None
        self.time = 0
        self.memory = 0
        self.verdict = 'Rejected'
        self.result = {}

        if self.submission.contest:
            self.contest = Contest.objects.get(id=self.submission.contest_id)
            self.rating = ContestRating.objects.get(contest=self.contest, user=self.submission.user)

    def prepared_data(self):
        data = {
            'source_code': self.submission.source_code,
            'language_id': self.submission.language,
            'stdin': self.test.input.read(),
            'expected_output': self.test.output.read(),
            'cpu_time_limit': self.problem.time_limit / 1000,
            'memory_limit': self.problem.memory_limit * 1000,
        }

        return data

    def get_result(self, token):
        try:
            response = requests.get(f'http://localhost/submissions/{token}',
                                    params={'base64_encoded': 'false',
                                            'wait': 'false'})
        except Exception as e:
            print(e)
            time.sleep(0.1)
            return self.get_result(token)
        else:
            if response.json().get('status', {}).get('id') in [1, 2]:
                time.sleep(1)
                return self.get_result(token)
            else:
                return response.json()

    def submit(self, data):
        try:
            response = requests.post('http://localhost/submissions/', data=data, params={'base64_encoded': 'false',
                                                                                         'wait': 'false'})
            return response.json()
        except Exception as e:
            time.sleep(1)
            logger.exception(e)
            return self.submit(data)

    def update_rating(self):
        if self.rating:
            problem_id = self.problem.pid
            if self.rating.verdicts[problem_id] != 1 and self.verdict == 'Accepted':
                self.rating.solved_count = F('solved_count') + 1
                self.rating.verdicts[problem_id] = 1
                self.rating.penalties[problem_id] += (
                                                             self.submission.submit_time - self.contest.start_time).total_seconds() // 60
                self.rating.penalty = F('penalty') + int(
                    (self.submission.submit_time - self.contest.start_time).total_seconds() // 60)
            elif self.rating.verdicts[problem_id] != 1 and self.verdict != 'Accepted':
                self.rating.verdicts[problem_id] = -1
                self.rating.penalties[problem_id] += 10
                self.rating.penalty = F('penalty') + 10
            else:
                pass

            self.rating.save()
            logger.info(f'Updated rating !', 'green')
        else:
            logger.info(f'This is not contest submission !')

    def save(self):
        self.submission.verdict = self.verdict
        self.submission.memory = self.memory
        self.submission.time = self.time

        self.submission.save()

    def update(self):
        logger.info(f'Result: {str(self.result)}')

        self.verdict = self.result.get('status', {}).get('description', 'Rejected')
        self.time = max(self.time, int(float(self.result.get('time', '0')) * 1000))
        self.memory = max(self.memory, self.result.get('memory', 0))

    def judge(self):
        logger.info(f'Judging submission with id {self.submission.id} to problem {self.problem.title}')

        for test in self.tests:
            self.test = test
            data = self.prepared_data()
            token = self.submit(data).get('token')
            self.result = self.get_result(token)
            self.update()

            if self.result.get('status', {}).get('id', None) != 3:
                break

        self.update_rating()
        self.save()
