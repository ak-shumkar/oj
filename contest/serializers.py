from rest_framework import serializers
from django.db.models import Q

from .models import Contest, ContestRating
from problem.serializers import ProblemSerializer
from problem.models import Problem
from submission.serializers import SubmissionListSerializer, SubmissionSerializer
from submission.models import Submission
import time


class ContestSerializer(serializers.ModelSerializer):
    duration = serializers.ReadOnlyField(source='contest_duration')
    until_contest = serializers.ReadOnlyField(source='before_contest')
    time_left = serializers.ReadOnlyField(source='before_finish')
    user = serializers.ReadOnlyField(source='author.username')
    title = serializers.ReadOnlyField(source='get_title')
    problem_count = serializers.ReadOnlyField(source='problems.count')

    class Meta:
        model = Contest
        fields = ('id', 'name', 'rule', 'level', 'description', 'start_time', 'end_time',
                  'duration', 'until_contest', 'time_left', 'user', 'title', 'problem_count')


class AdminContestDetailSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(read_only=True, many=True)
    pids = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = ('id', 'name', 'rule', 'author', 'problems', 'pids')

    def get_pids(self, instance):
        problems = Problem.objects.filter(contest=instance)
        pids = [problem.pid for problem in problems]
        return pids


class ContestRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestRating
        fields = ('contest', 'user')


class ContestRankingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    total_penalty = serializers.ReadOnlyField()
    problems_count = serializers.ReadOnlyField(source='contest.problems.count')

    class Meta:
        model = ContestRating
        fields = '__all__'
