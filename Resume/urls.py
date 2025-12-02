from django.urls import path
from .views import (
    ResumeHomeView,
    ResumeListView,
    ResumeDetailView,
)

app_name = 'resume'

urlpatterns = [
    path('', ResumeHomeView.as_view(), name='home'),
    path('employees/', ResumeListView.as_view(), name='resume_list'),
    path('employees/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
]
