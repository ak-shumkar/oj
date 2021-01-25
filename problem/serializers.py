from rest_framework import serializers
from .models import Problem, Test


class ProblemSerializer(serializers.ModelSerializer):
    test_count = serializers.IntegerField(source='tests.count', read_only=True)
    class Meta:
        model = Problem
        fields = '__all__'
        extra_fields = ('test_count',)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


