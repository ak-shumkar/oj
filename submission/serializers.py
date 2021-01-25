from rest_framework.serializers import ModelSerializer
from .models import Submission


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('user', 'source_code', 'contest', 'submit_time', 'problem', 'language')


class SubmissionListSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


