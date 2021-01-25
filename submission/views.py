import json
from datetime import datetime
import requests
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from judge.tasks import judge_task
from .models import Submission
from contest.models import ContestRating, Contest
from .serializers import SubmissionSerializer, SubmissionListSerializer


class SubmissionListAPI(ListAPIView):
    serializer_class = SubmissionListSerializer
    queryset = Submission.objects.all()


class SubmissionAPI(CreateAPIView, UpdateAPIView):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print('in data : ', request.data)
        data = request.data
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            print('Here')
            raise ValidationError({'detail': serializer.errors})
        instance = serializer.save()
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
        if data['submit_time'] > contest.end_time.strftime("%Y-%m-%d %H:%M:%S"):
            # raise ValidationError({'error': 'Contest is over'})
            print('Contest is over')
            del data['contest']
            print('new data : ', data)
            print(request.headers)
            r = requests.post('http://127.0.0.1:8000/api/submission/', data=json.dumps(data), headers=request.headers)
            return Response(data=r.json(), status=r.status_code)

        if data['submit_time'] < contest.start_time.strftime("%Y-%m-%d %H:%M:%S"):
            raise ValidationError({'error': 'Contest is coming'})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.save()

        judge_task.delay(instance.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


