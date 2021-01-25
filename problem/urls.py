from django.urls import path, include
from .views import ProblemListAPI, TestViewSet, AddContestProblemAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tests', TestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/contest/problem/', AddContestProblemAPI.as_view()),
    path('problems/', ProblemListAPI.as_view())
]