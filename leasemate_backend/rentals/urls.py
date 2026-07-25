from django.urls import path
from .views import RentListingCreateView, RentListView, ChatWithOwnerView

urlpatterns = [
    path('listings/', RentListView.as_view(), name='rent-list'),
    path('listings/create/', RentListingCreateView.as_view(), name='rent-listing-create'),
    path('listings/<int:rent_listing_id>/chat/', ChatWithOwnerView.as_view(), name='chat-with-owner'),
]
