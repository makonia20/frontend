from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import LeasemateUser

class AuthenticationTests(TestCase):
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
        self.login_url = reverse('login')  # Adjust if the URL name is different

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],  # Use username for login
            'password': '123456'  # Updated to match the user's password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],  # Use username for login
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
