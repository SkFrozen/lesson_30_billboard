from django.test import Client, TestCase
from django.urls import reverse
from users.models import User


class TestCreateUserPermissions(TestCase):
    """
    Testing user permissions to create user
    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse("user_list_create")
        cls.superuser = User.objects.create_superuser(
            "admin1", "admin@mail.com", "admin"
        )
        cls.user = User.objects.create_user("pasha1", "pasha@mail.com", "pasha")

    def test_create_user_by_anonymous(self):
        response = self.client.post(
            self.url,
            {
                "username": "test",
                "email": "test@mail.com",
                "password": "test",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_cant_read_user_list_by_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_cant_read_user_list_by_commonuser(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        print(response)
        self.assertEqual(response.status_code, 403)

    def test_can_read_user_list_by_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_paginate_users_list(self):
        self.client.force_login(self.superuser)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, "Error when getting list of users")
        self.assertIn("count", response.data, "Response have not got users count")
        self.assertGreater(len(response.data["results"]), 0)
