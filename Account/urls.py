from django.urls import path
from . import views

app_name = 'account'   # برای استفاده از نام‌های معنادار در template

urlpatterns = [
    path('', views.AccountHomeView.as_view(), name='home'),  # /account/
    path('users/', views.PersonalInfoListView.as_view(), name='user_list'),  # /account/users/
    path('users/<int:pk>/', views.PersonalInfoListView.as_view(), name='user_detail'),  # /account/users/1/
]
