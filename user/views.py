from rest_framework import viewsets, permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView

from .models import User, Profile
from .serializers import AccountCreateSerializer, LoginSerializer, UserProfileSerializer, UserDetailSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegisterAPI(CreateAPIView):
    serializer_class = AccountCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        # if User.objects.filter(username=data['username']).exists():
        #     return Response({'error': "This username is taken"}, status=status.HTTP_400_BAD_REQUEST)
        # if User.objects.filter(email=data['email']).exists():
        #     return Response({'error': "This email is taken"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Profile.objects.create(user=user)
        #
        # return Response({
        #     "user": AccountCreateSerializer(user, context=self.get_serializer_context()).data
        # }, status=status.HTTP_201_CREATED)

        return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny, )


class ProfileViewAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'account'


class UserDetailAPI(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


class UserListAPI(ListAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

