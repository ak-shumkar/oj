
import json
import requests
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from contest.models import ContestRating, Contest
from judge.tasks import judge_task
from .models import Submission
from .serializers import SubmissionSerializer, SubmissionListSerializer


class SubmissionListAPI(ListAPIView):
    """
    View to get list of submissions
    Option: Filter by contest id
    """
    serializer_class = SubmissionListSerializer
    queryset = Submission.objects.all()
    pagination_class = LimitOffsetPagination
    lookup_field = 'contest'

    def get_queryset(self):
        contest_id = self.kwargs.get(self.lookup_field, None)
        qs = self.queryset
        if contest_id:
            qs = qs.filter(contest_id=contest_id)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubmissionAPI(CreateAPIView):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            raise ValidationError({'detail': serializer.errors})
        instance = serializer.save()
        setattr(instance, 'verdict', 'Judging...')
        instance.save()

        judge_task.delay(instance.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContestSubmissionPermission(permissions.BasePermission):
    message = 'You have not registered for this contest'

    def has_permission(self, request, view):
        user = request.data.get('user')
        if not ContestRating.objects.filter(user_id=user).exists():
            return False
        return True


class ContestSubmissionAPI(CreateAPIView):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()
    permission_classes = (permissions.IsAuthenticated, ContestSubmissionPermission)

    def post(self, request, *args, **kwargs):
        data = request.data

        contest_id = data.get('contest')
        if not contest_id:
            return Response({'error': 'Contest is missing'}, status=status.HTTP_400_BAD_REQUEST)

        contest = Contest.objects.get(id=contest_id)
        if data['submit_time'] > contest.end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"):
            # raise ValidationError({'error': 'Contest is over'})
            print('Contest is over')
            del data['contest']
            print(request.headers)
            r = requests.post('http://127.0.0.1:8000/api/submission/', data=json.dumps(data), headers=request.headers)
            return Response(data=r.json(), status=r.status_code)

        if data['submit_time'] < contest.start_time.strftime("%Y-%m-%d %H:%M:%S"):
            raise ValidationError({'error': 'Contest is coming'})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        setattr(instance, 'verdict', 'Judging...')
        instance.save()

        judge_task.delay(instance.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


