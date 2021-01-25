from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import ContestRating, Contest
from .serializers import ContestRegisterSerializer, ContestSerializer, ContestRankingSerializer, AdminContestDetailSerializer


# Admin APIs
class ContestCreateAPI(generics.CreateAPIView):
    serializer_class = ContestSerializer
    queryset = Contest.objects.all()
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            assert data['start_time'] < data['end_time']
        except AssertionError:
            return Response(data={'error': 'Wrong date settings'}, status=status.HTTP_400_BAD_REQUEST, headers=None)

        return super().create(request, *args, **kwargs)


class ContestEditAPI(generics.UpdateAPIView):
    serializer_class = ContestSerializer
    queryset = Contest.objects.all()
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class AdminContestDetailAPI(generics.RetrieveAPIView):
    serializer_class = AdminContestDetailSerializer
    queryset = Contest.objects.all()
    permission_classes = (IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        print('request_data: ', request.data)
        print('kwargs: ', kwargs)
        return super().retrieve(request, *args, **kwargs)


# User APIs
class ContestListAPI(generics.ListAPIView):
    serializer_class = ContestSerializer
    queryset = Contest.objects.all()

    def get_queryset(self):
        phase = self.request.query_params.get('phase')
        if phase == 'past':
            return super().get_queryset().filter(end_time__lt=now())
        elif phase == 'future':
            return super().get_queryset().filter(start_time__gt=now())
        elif phase == 'ongoing':
            return super().get_queryset().filter(start_time__lt=now(), end_time__gt=now())

        author = self.request.query_params.get('author')
        if author:
            return super().get_queryset().filter(author=author)

        return super().get_queryset()


class ContestDetailAPI(generics.RetrieveAPIView):
    serializer_class = ContestSerializer
    queryset = Contest.objects.all()

    def get(self, request, *args, **kwargs):
        print('request_data: ', request.data)
        print('kwargs: ', kwargs)
        return super().get(request, *args, **kwargs)


class ContestRegisterAPI(generics.CreateAPIView):
    queryset = ContestRating.objects.all()
    serializer_class = ContestRegisterSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Handle contest registration
        contest_id = request.data['contest']
        contest = Contest.objects.get(id=contest_id)
        # if now() > contest.start_time:
        #     raise ValidationError({'detail': 'Registration has ended'})

        return super().post(request, *args, **kwargs)


class ContestRankingAPI(generics.ListAPIView):
    serializer_class = ContestRankingSerializer
    queryset = ContestRating.objects.all()

    def get_queryset(self):
        contest_id = self.request.query_params.get('contest')
        return super().get_queryset().filter(contest_id=contest_id)


@api_view()
def is_registered(request):
    user_id = request.query_params.get('user')
    if not user_id:
        return Response({'error': 'User missing'}, status=status.HTTP_400_BAD_REQUEST)

    contest_id = request.query_params.get('contest')
    if not contest_id:
        return Response({'error': 'Contest missing'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ContestRating.objects.filter(contest_id=contest_id, user_id=user_id)

    except ContestRating.DoesNotExist:
        return Response({'result': False}, status=status.HTTP_200_OK)

    return Response({'result': True}, status=status.HTTP_200_OK)