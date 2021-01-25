from django.urls import path
from .views import SubmissionAPI, SubmissionListAPI, ContestSubmissionAPI


urlpatterns = [
    path('submission/', SubmissionAPI.as_view()),
    path('contest_submission/', ContestSubmissionAPI.as_view()),
    path('submissions/', SubmissionListAPI.as_view()),
]