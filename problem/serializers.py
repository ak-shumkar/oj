from rest_framework import serializers
from .models import Problem, Test, Editorial
from submission.models import Submission


class ProblemSerializer(serializers.ModelSerializer):
    test_count = serializers.IntegerField(source='tests.count', read_only=True)
    solved = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = '__all__'
        extra_fields = ('test_count',)

    def get_solved(self, instance):
        user = self.context['request'].user
        if not user.id:
            return 0

        submissions = Submission.objects.filter(problem=instance, user=user)

        if submissions:
            accepted = submissions.filter(verdict='Accepted')
            if accepted:
                return 1
            else:
                return -1
        else:
            return 0


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class EditorialSerializer(serializers.ModelSerializer):
    pid = serializers.ReadOnlyField(source='problem.pid')
    title = serializers.ReadOnlyField(source='problem.title')
    class Meta:
        model = Editorial
        fields = '__all__'