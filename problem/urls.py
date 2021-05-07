from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tests', views.TestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/contest/problem/', views.AddContestProblemAPI.as_view(), name='create_contest_problem'),
    path('admin/contest/problem/<pk>/', views.ProblemEditAPI.as_view(), name='create_contest_problem'),
    path('problems/', views.ProblemListAPI.as_view()),
    path('problems/<int:pk>/', views.ProblemDetailAPI.as_view()),
    path('problems/<int:problem>/editorial/', views.EditorialRetrieveView.as_view()),
    path('contests/<int:contest>/editorial/', views.EditorialListView.as_view()),
]