from django.urls import path
from .views import (
    JobRequestHomeView,
    JobRequestListView,
    JobRequestDetailView,
    JobRequestCreateView,
    JobRequestUpdateView,
)

app_name = 'jobrequest'

urlpatterns = [
    path('', JobRequestHomeView.as_view(), name='home'),
    path('all/', JobRequestListView.as_view(), name='request_list'),
    path('create/', JobRequestCreateView.as_view(), name='create_request'),       # ثبت درخواست جدید
    path('<int:pk>/edit/', JobRequestUpdateView.as_view(), name='request_edit'),  # ویرایش درخواست
    path('<int:pk>/', JobRequestDetailView.as_view(), name='request_detail'),
]
