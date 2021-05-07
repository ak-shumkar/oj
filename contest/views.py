from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import ContestRating, Contest
from .serializers import ContestRegisterSerializer, ContestSerializer, ContestRankingSerializer, \
    AdminContestDetailSerializer


# *************************** Admin APIs *****************************************************************
class ContestCreateAPI(generics.CreateAPIView):
    """
    Admin view to create contest
    :return Bad requests if contest start time is bigger than contest end time. Otherwise success.
    """
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
    """
    Admin view to edit contest details.
    :exception Contest cannot be edited if it is running or finished
    """
    serializer_class = ContestSerializer
    queryset = Contest.objects.all()
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        try:
            # assert it is future contest TODO
            pass
        except AssertionError:
            return Response(data={'error': 'Contest cannot be edited, as it is finished or running'}, status=status.HTTP_400_BAD_REQUEST, headers=None)

        return super().put(request, *args, **kwargs)


class AdminContestDetailAPI(generics.RetrieveAPIView):
    """
    Admin view to get contest details. Only author of the contest can view details TODO
    """
    serializer_class = AdminContestDetailSerializer
    queryset = Contest.objects.all()
    # permission_classes = (IsAdminUser,)  # TODO

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


# ********************************** User APIs ******************************************************************
class ContestListAPI(generics.ListAPIView):
    """
    View to list contests. Filter by its phase.
    Also filter by author of the contest.
    """
    serializer_class = ContestSerializer
    queryset = Contest.objects.all()

    def get_queryset(self):
        phase = self.request.query_params.get('phase')
        if phase == 'past':
            return super().get_queryset().filter(end_time__lt=now())
        elif phase == 'active':
            return super().get_queryset().filter(end_time__gte=now())

        author = self.request.query_params.get('author')
        if author:
            return super().get_queryset().filter(author=author)

        return super().get_queryset()


class ContestDetailAPI(generics.RetrieveAPIView):
    """
    View for contest details. Avoid to return sensible detail TODO
    """
    serializer_class = ContestSerializer
    queryset = Contest.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ContestRegisterAPI(generics.CreateAPIView):
    """
    Contest registration view
    """
    queryset = ContestRating.objects.all()
    serializer_class = ContestRegisterSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        :raise -> Validation error if contest has started or ended or registration has ended
        """
        # Handle contest registration
        contest_id = request.data['contest']
        contest = Contest.objects.get(id=contest_id)

        if now() > contest.start_time:
            raise ValidationError({'detail': 'Registration has ended'})

        return super().post(request, *args, **kwargs)


class ContestRankingAPI(generics.ListAPIView):
    """
    Contest ranking view
    """
    serializer_class = ContestRankingSerializer
    queryset = ContestRating.objects.all()
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """
        :return: List of rankings of specific contest
        """
        contest_id = self.request.query_params.get('contest')
        qs = self.queryset.filter(contest_id=contest_id)
        return qs

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


@api_view()
def is_registered(request):
    """
    Check if user is registered in contest
    :param request:
    :return: `True` if registered, otherwise `False`
    """
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
