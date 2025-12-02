from django.urls import path
from .views import (
    UserPanelHomeView,
    UserPanelListView,
    UserPanelDetailView,
)

app_name = 'userpanel'

urlpatterns = [
    path('', UserPanelHomeView.as_view(), name='home'),
    path('list/', UserPanelListView.as_view(), name='panel_list'),
    path('<int:pk>/', UserPanelDetailView.as_view(), name='panel_detail'),
]
