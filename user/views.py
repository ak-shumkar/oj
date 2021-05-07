import json

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Profile
from .serializers import AccountCreateSerializer, LoginSerializer, UserProfileSerializer, UserDetailSerializer


def send_email(user):
    """
    :param user: User instance that mail have to be sent
    :return: None
    """

    verify_link = settings.FRONTEND_URL + 'email-verify/' + user.verification_token
    subject, from_email, to = 'Verify Your Email', 'mm.kalandar@gmail.com', user.email
    html_content = render_to_string('verify-email.html',
                                    {'verify_link': verify_link,
                                     'base_url': settings.FRONTEND_URL,
                                     'username': user.username
                                     })
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


class UserRegisterAPI(CreateAPIView):
    """
    User registration API
    """
    serializer_class = AccountCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return: Return bad request if username or email is taken. Otherwise, return created account details
        """
        data = request.data
        if User.objects.filter(username=data['username']).exists():
            return Response({'error': "This username is taken"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=data['email']).exists():
            return Response({'error': "This email is taken"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # -> Set random token for user. This token is used to activate account
        user.verification_token = get_random_string(length=32)
        user.save()

        # -> Immediately send verification link to user's email
        # send_email(user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


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


@api_view(http_method_names=['POST'])
def validate_email_token(request):
    data = json.loads(request.body.decode('utf-8'))
    token = data['token']
    res = {
        'status': 'success',
        'message': 'Valid',
    }

    try:
        user = User.objects.get(verification_token=token, is_active=False)
        user.is_active = True
        user.save()

    except User.DoesNotExist:
        res = {
            'status': 'failed',
            'message': 'Invalid',
        }

    return Response(res, status=status.HTTP_200_OK)

