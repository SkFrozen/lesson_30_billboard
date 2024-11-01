from datetime import datetime, timedelta

from django.test import Client, TestCase
from users.models import User

from ..models import Event


class TestEventSubscribe(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = "/api/v1/events/"
        cls.user = User.objects.create(username="test", password="test123")
        Event.objects.create(
            title="test",
            description="test",
            meeting_time=datetime.now() + timedelta(days=15),
        )
        Event.objects.create(
            title="test2",
            description="test2",
            meeting_time=datetime.now() - timedelta(days=15),
        )

    def test_cant_subscribe_event_by_anonymous(self):
        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, 401)

    def test_can_subscribe_event_by_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url + "1/")
        self.assertEqual(response.status_code, 201, response.content)

    def test_cant_subscribe_passed_event(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url + "2/")
        self.assertEqual(response.status_code, 404, response.content)
