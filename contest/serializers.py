from rest_framework import serializers
from .models import Contest, ContestRating
from problem.serializers import ProblemSerializer
from submission.serializers import SubmissionListSerializer, SubmissionSerializer
from submission.models import Submission


class ContestSerializer(serializers.ModelSerializer):
    duration = serializers.ReadOnlyField(source='contest_duration')
    until_contest = serializers.ReadOnlyField(source='before_contest')
    time_left = serializers.ReadOnlyField(source='before_finish')
    user = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Contest
        fields = '__all__'
        extra_fields = ('duration', 'until_contest', 'time_left', 'user')


class AdminContestDetailSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(read_only=True, many=True)

    class Meta:
        model = Contest
        fields = ('id', 'name', 'rule', 'author', 'problems')


class ContestRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestRating
        fields = ('contest', 'user')


class ContestRankingSerializer(serializers.ModelSerializer):
    user_submission = serializers.SerializerMethodField()

    def get_user_submission(self, instance):
        try:
            submission = Submission.objects.filter(user=instance.user_id, contest=instance.contest_id).order_by('verdict').first()
            return SubmissionListSerializer(submission).data
        except Exception as e:
            return {}

    class Meta:
        model = ContestRating
        fields = '__all__'
        extra_fields = ('user_submission',)


