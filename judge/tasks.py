from celery import shared_task
from judge.judger import Judger


@shared_task
def judge_task(submission_id):
    print('Task has started')
    Judger(submission_id).judge()
