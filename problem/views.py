from django.db.models import Q
from django.utils.timezone import now

from rest_framework import permissions, generics, pagination
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from config.const import L
from contest.models import Contest
from .models import Problem, Test, Editorial
from user.models import User
from .serializers import ProblemSerializer, TestSerializer, EditorialSerializer


class ProblemListAPI(generics.ListAPIView):
    serializer_class = ProblemSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Problem.objects.all()
    pagination_class = pagination.LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if 'contest' in self.request.query_params:
            contest = self.request.query_params['contest']
            return super().get_queryset().filter(contest=contest).order_by('pid')
        return super().get_queryset().filter(contest__end_time__lt=now())

    def list(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: List of ordered rankings in specific page
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProblemDetailAPI(generics.RetrieveAPIView):
    serializer_class = ProblemSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Problem.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    # def get_queryset(self):
    #     if 'contest' in self.request.query_params:
    #         contest = self.request.query_params['contest']
    #         return super().get_queryset().filter(contest=contest)
    #     return super().get_queryset()


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


class ProblemEditAPI(generics.UpdateAPIView):
    serializer_class = ProblemSerializer
    queryset = Problem.objects.all()

    # def post(self, request, *args, **kwargs):
    #     data = request.data
    #     print('Custom data : ', data)
    #     try:
    #         contest = Contest.objects.get(id=data["contest"])
    #         user = User.objects.get(id=data["author"])
    #     except (Contest.DoesNotExist, User.DoesNotExist):
    #         raise ValidationError({'detail': "Contest or author does not exist"})
    #
    #     # if contest.phase != 'future':
    #     #     raise ValidationError({'detail': 'Contest has started or over'})
    #     if Problem.objects.filter(contest=contest, _id=data["_id"]).exists():
    #         raise ValidationError({'detail': "Duplicate problem id in this contest"})
    #
    #     return super().post(request, *args, **kwargs)


class EditorialListView(generics.ListAPIView):
    serializer_class = EditorialSerializer
    queryset = Editorial.objects.all()
    lookup_field = 'contest'

    def get_queryset(self):
        contest_id = self.kwargs[self.lookup_field]
        print('lookup field', self.kwargs[self.lookup_field])
        return self.queryset.filter(Q(problem__contest_id=contest_id), Q(problem__contest__end_time__lt=now()))


class EditorialRetrieveView(generics.RetrieveAPIView):
    settings = EditorialSerializer
    queryset = Editorial.objects.all()
    lookup_field = 'problem'

    def get_queryset(self):
        problem_id = self.lookup_field
        return self.queryset.get(Q(problemid=problem_id))
