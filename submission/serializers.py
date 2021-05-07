from rest_framework import serializers
from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('user', 'source_code', 'contest', 'submit_time', 'problem', 'language')


class SubmissionListSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    problem_title = serializers.ReadOnlyField(source='problem.title')

    class Meta:
        model = Submission
        fields = '__all__'


