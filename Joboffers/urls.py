from django.urls import path
from .views import (
    JobOfferListView,
    JobOfferDetailView,
    JobPositionListView,
    JobCategoryListView,
)

app_name = 'joboffers'

urlpatterns = [
    path('', JobOfferListView.as_view(), name='offer_list'),
    path('<int:pk>/', JobOfferDetailView.as_view(), name='offer_detail'),
    path('positions/', JobPositionListView.as_view(), name='position_list'),
    path('categories/', JobCategoryListView.as_view(), name='category_list'),
]
