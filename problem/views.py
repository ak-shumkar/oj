import re

from rest_framework import permissions, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from config.const import L
from contest.models import Contest
from .models import Problem, Test
from user.models import User
from .serializers import ProblemSerializer, TestSerializer


class ProblemListAPI(generics.ListAPIView):
    serializer_class = ProblemSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Problem.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if 'contest' in self.request.query_params:
            contest = self.request.query_params['contest']
            return super().get_queryset().filter(contest=contest)
        return super().get_queryset()


class TestViewSet(ModelViewSet):
    serializer_class = TestSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Test.objects.all()
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        problem = self.request.query_params['problem']
        return super().get_queryset().filter(problem=problem)


class AddContestProblemAPI(generics.CreateAPIView):
    serializer_class = ProblemSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        print('Custom data : ', data)
        try:
            contest = Contest.objects.get(id=data["contest"])
            user = User.objects.get(id=data["author"])
        except (Contest.DoesNotExist, User.DoesNotExist):
            raise ValidationError({'detail': "Contest or author does not exist"})

        # if contest.phase != 'future':
        #     raise ValidationError({'detail': 'Contest has started or over'})
        if Problem.objects.filter(contest=contest, _id=data["_id"]).exists():
            raise ValidationError({'detail': "Duplicate problem id in this contest"})

        return super().post(request, *args, **kwargs)


