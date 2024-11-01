from django.test import TestCase
from users.models import User
from users.serializers import UserSerializer


class TestUserSerializer(TestCase):

    def test_user_serializer_password_encrypt(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testuser",
        }
        serializer = UserSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        user = User.objects.get(username="testuser")
        self.assertIn("pbkdf2_sha256", user.password)
        self.assertNotEqual(user.password, "testuser")
