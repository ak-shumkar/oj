from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Profile


class AccountCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for account creation. Set active to `False`. It will be set to `True` when
    user activates his account
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    fullname = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile', 'fullname')


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer, TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Wrong password',
        'no_user': 'User does not exist'
    }

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if not username:
            raise serializers.ValidationError('Username is required')
        if not password:
            raise serializers.ValidationError('Password is required')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_user']
            )

        user = authenticate(username=username, password=password)
        data = super().validate(data)

        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        update_last_login(None, self.user)

        return data

    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        field = '__all__'

