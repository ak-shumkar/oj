from rest_framework.routers import DefaultRouter
from .views import ContestCreateAPI, ContestListAPI, \
    ContestRegisterAPI, ContestDetailAPI, \
    ContestRankingAPI, ContestEditAPI, is_registered, AdminContestDetailAPI
from django.urls import path
router = DefaultRouter()

urlpatterns = [
    path('admin/contest/', ContestCreateAPI.as_view()),
    path('admin/contest/edit/<pk>', ContestEditAPI.as_view()),
    path('admin/contest/<pk>', AdminContestDetailAPI.as_view()),
    path('contests/', ContestListAPI.as_view()),
    path('contests/<pk>', ContestDetailAPI.as_view()),
    path('contests/register/', ContestRegisterAPI.as_view()),
    path('contests/ranking/', ContestRankingAPI.as_view()),
    path('contests/registered_user/', is_registered),
]
