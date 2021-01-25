from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from .views import UserRegisterAPI, LoginAPI, ProfileViewAPI, UserDetailAPI, UserListAPI

router = DefaultRouter()

urlpatterns = [
    path('account/login/', LoginAPI.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('account/register/', UserRegisterAPI.as_view(), name='create_user'),
    path('profile/', ProfileViewAPI.as_view()),
    path('profiles/<username>/', UserDetailAPI.as_view()),
    path('users/', UserListAPI.as_view()),
]