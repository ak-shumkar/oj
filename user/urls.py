from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from . import views

router = DefaultRouter()

urlpatterns = [
    path('account/login/', views.LoginAPI.as_view(), name='login'),
    path('account/register/', views.UserRegisterAPI.as_view(), name='create_user'),
    path('account/validate-email-token/', views.validate_email_token, name='create_user'),
    path('profile/', views.ProfileViewAPI.as_view()),
    path('profiles/<username>/', views.UserDetailAPI.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserListAPI.as_view()),
    re_path('users/current/$', views.UserListAPI.as_view()),
]
