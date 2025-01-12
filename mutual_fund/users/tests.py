from rest_framework.test import APITestCase
from django.urls import reverse

class AccountsTestCase(APITestCase):
    def test_register(self):
        data = {
            "email": "shreya@shreya.com",
            "password": "password",
            "username": "shreya"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        self.test_register()
        data = {
            "email": "shreya@shreya.com",
            "password": "password"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)

        data["password"] = "wrongpassword"
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 401)