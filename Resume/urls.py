from django.urls import path
from .views import ResumeHomeView, ResumeListView, ResumeDetailView, ResumeInfoView

app_name = 'resume'

urlpatterns = [
    path('', ResumeHomeView.as_view(), name='resume_home'),
    path('list/', ResumeListView.as_view(), name='resume_list'),
    path('detail/<int:pk>/', ResumeDetailView.as_view(), name='resume_detail'),
    path('info/', ResumeInfoView, name='resume_add'),
]
