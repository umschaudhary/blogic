from django.urls import reverse
from rest_framework.test import APITestCase


class UserTest(APITestCase):

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

    def test_create_user(self):
        data = self.get_data()
        url = self.url
        response = self.client.post(
            path=url,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        return response

    def test_update(self):
        response = self.test_create_user()
        username = response.data.get('username')
        phone_number = response.data.get('phone_number')
        self.client.login(
            phone_number=phone_number,
            password='admin123'
        )
        url = reverse("api_v1:users:users-detail",
                      kwargs={'username': username})
        data = self.get_data()
        data['full_name'] = "Ramesh"

        response = self.client.put(
            path=url,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('full_name'), 'Ramesh')

    def test_user_profile(self):
        response = self.test_create_user()
        phone_number = response.data.get('phone_number')
        url = reverse("api_v1:users:users-me")

        self.client.login(
            phone_number=phone_number,
            password='admin123'
        )
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_without_login(self):
        url = reverse("api_v1:users:users-me")
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 401)
