from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


app_name = 'account'

urlpatterns = [
    path('', views.AccountHomeView.as_view(), name='home'),
    path('users/', views.PersonalInfoListView.as_view(), name='user_list'),
    path('users/add/', views.PersonalInfoCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.PersonalInfoUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/', views.PersonalInfoDetailView.as_view(), name='user_detail'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='account:login'), name='logout'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
]
