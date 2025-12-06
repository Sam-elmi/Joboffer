from django.urls import path
from .views import (
    JobOfferListView,
    JobOfferDetailView,
    JobOfferCreateView,
    JobCategoryListView,
    JobCategoryCreateView,
    JobOfferDeleteView,
    JobOfferUpdateView

)

app_name = 'joboffers'

urlpatterns = [
    path('', JobOfferListView.as_view(), name='offer_list'),
    path('<int:pk>/', JobOfferDetailView.as_view(), name='offer_detail'),
    path('add/', JobOfferCreateView.as_view(), name='offer_add'),
    path('<int:pk>/edit/', JobOfferUpdateView.as_view(), name='offer_edit'),
    path('<int:pk>/delete/', JobOfferDeleteView.as_view(), name='offer_delete'),
    path('categories/', JobCategoryListView.as_view(), name='category_list'),
    path('categories/add/', JobCategoryCreateView.as_view(), name='category_add'),

]
