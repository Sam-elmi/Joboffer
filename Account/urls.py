from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('', views.AccountHomeView.as_view(), name='home'),
    path('users/', views.PersonalInfoListView.as_view(), name='user_list'),
    path('users/add/', views.PersonalInfoCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.PersonalInfoUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/', views.PersonalInfoDetailView.as_view(), name='user_detail'),
    path('login/', views.LoginView.as_view(template_name='account/login.html'), name='login'),
]
