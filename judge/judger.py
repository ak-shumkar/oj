from problem.models import Problem, Test
from submission.models import Submission
import requests
import time


class Judger:
    def __init__(self, submission_id):
        self.submission = Submission.objects.get(id=submission_id)
        self.problem = Problem.objects.get(id=self.submission.problem_id)
        self.tests = Test.objects.filter(problem=self.problem)
        self.test = None
        self.time = 0
        self.memory = 0
        self.verdict = 'Judging ...'
        self.result = {}

    def prepared_data(self):
        data = {
            'source_code': self.submission.source_code,
            'language_id': 76,
            'stdin': self.test.input.read(),
            'expected_output': self.test.output.read(),
            'cpu_time_limit': self.problem.time_limit / 1000,
            'memory_limit': self.problem.memory_limit * 1000,
        }

        return data

    # Submission result from judger
    def get_result(self, token):
        try:
            r = requests.get('http://localhost/submissions/{}'.format(token), params={'base64_encoded': 'false',
                                                                                      'wait': 'false'})
        except Exception as e:
            print(e)
            time.sleep(1)
            return self.get_result(token)
        else:
            if r.json().get('status', {}).get('id') in [1, 2]:
                time.sleep(1)
                # print(r.json())
                return self.get_result(token)
            else:
                return r.json()

    def submit(self, data):
        try:
            response = requests.post('http://localhost/submissions/', data=data, params={'base64_encoded': 'false',
                                                                                         'wait': 'false'})
            return response.json()
        except Exception as e:
            time.sleep(1)
            print(e)
            return self.submit(data)

    def judge(self):
        print('Judging submission with id {} to problem {}'.format(self.submission.id, self.problem.title))
        self.submission.verdict = 'Judging ...'
        self.submission.save()

        for test in self.tests:
            self.test = test
            data = self.prepared_data()

            token = self.submit(data).get('token')

            self.result = self.get_result(token)
            print('time : ', int(float(self.result.get('time')) * 1000))
            self.verdict = self.result.get('status', {}).get('description')
            self.time = max(self.time, int(float(self.result.get('time')) * 1000))
            self.memory = max(self.memory, self.result.get('memory'))
            if self.result.get('status', {}).get('id') != 3:
                break

        self.submission.verdict = self.verdict
        self.submission.memory = self.memory
        self.submission.time = self.time

        self.submission.save()

