from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import RentListing
from leasemate_authentication.models import LeasemateUser

class RentListingTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'ashleymakoni',  # New username field
            'phone': '0771883091',
            'id_number': '42-311120x42',
            'first_name': 'Ashley',
            'middle_name': 'Tadiswa',
            'last_name': 'Makoni',
            'password': '123456'  # Password for the user
        }
        self.user = LeasemateUser.objects.create_user(**self.user_data)
        self.user.save()
        self.login_url = reverse('login')  # Adjust if the URL name is different
        self.rent_listing_url = reverse('rent-listing-create')  # Adjust if the URL name is different

    def login_user(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])  # Log in the user

    def test_create_rent_listing_success(self):
        self.login_user()  # Ensure the user is logged in
        response = self.client.post(self.rent_listing_url, {
            'location': 'Test Location',
            'description': 'Test Description',
            'country': 'Test Country',
            'city': 'Test City',
            'roomDetails': 'Test Room Details',
            'price': 1000,
            'houseType': 'Flat',  # Use a valid choice
            'numberOfRooms': 2,
            'painted': 'Yes',  # Use string 'Yes' or 'No'
            'ceiling': 'Yes',  # Use string 'Yes' or 'No'
            'electricity': 'Yes',  # Use string 'Yes' or 'No'
            'solar': 'No',  # Use string 'Yes' or 'No'
            'durawalled': 'Yes',  # Use string 'Yes' or 'No'
            'fenced': 'Yes',  # Use string 'Yes' or 'No'
        })
        
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)  # Print the response data for debugging

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rent_listing_unauthenticated(self):
        response = self.client.post(self.rent_listing_url, {
            'location': 'Test Location',
            'description': 'Test Description',
            'country': 'Test Country',
            'city': 'Test City',
            'roomDetails': 'Test Room Details',
            'price': 1000,
            'houseType': 'Apartment',
            'numberOfRooms': 2,
            'painted': 'Yes',  # Use string 'Yes' or 'No'
            'ceiling': 'Yes',  # Use string 'Yes' or 'No'
            'electricity': 'Yes',  # Use string 'Yes' or 'No'
            'solar': 'No',  # Use string 'Yes' or 'No'
            'durawalled': 'Yes',  # Use string 'Yes' or 'No'
            'fenced': 'Yes',  # Use string 'Yes' or 'No'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_rent_listings(self):
        self.login_user()  # Ensure the user is logged in
        response = self.client.get(reverse('rent-list'))  # Adjust if the URL name is different
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chat_with_owner(self):
        self.login_user()  # Ensure the user is logged in
        rent_listing = RentListing.objects.create(
            user=self.user,
            location='Test Location',
            description='Test Description',
            country='Test Country',
            city='Test City',
            roomDetails='Test Room Details',
            price=1000,
            houseType='Apartment',
            numberOfRooms=2,
            painted=True,
            ceiling=True,
            electricity=True,
            solar=False,
            durawalled=True,
            fenced=True,
        )
        response = self.client.get(reverse('chat-with-owner', args=[rent_listing.id]))  # Adjust if the URL name is different
        self.assertEqual(response.status_code, status.HTTP_200_OK)
