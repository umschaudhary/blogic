from django.urls import reverse
from rest_framework.test import APITestCase
from apps.users.models import PhoneOtp


class UserInitialFLowTest(APITestCase):

    def setUp(self):
        self.url = reverse("api_v1:users:users-list")

    def get_data(self):
        return {
            "phone_number": "9800000000",
            "password": "admin123",
            "username": "newusername",
            "full_name": "Ums Chaudhary",
            "gender": "Male"
        }

    def test_user_register(self):
        url = self.url
        data = self.get_data()
        res = self.client.post(
            url,
            data,
            format='json',
        )
        self.assertEqual(201, res.status_code)
        return res.data.get('phone_number')
