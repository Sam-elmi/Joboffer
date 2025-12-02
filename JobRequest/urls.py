from django.urls import path
from .views import (
    JobRequestHomeView,
    JobRequestListView,
    JobRequestDetailView,
)

app_name = 'jobrequest'

urlpatterns = [
    path('', JobRequestHomeView.as_view(), name='home'),
    path('all/', JobRequestListView.as_view(), name='request_list'),
    path('<int:pk>/', JobRequestDetailView.as_view(), name='request_detail'),
]
