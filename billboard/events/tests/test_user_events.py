from datetime import datetime, timedelta

from django.test import Client, TestCase
from django.urls import reverse
from users.models import User

from ..models import Event


class TestUserEventList(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse("user_events")
        cls.user = User.objects.create_user(
            username="testname", password="testpass", email="test@test.com"
        )
        cls.event = Event.objects.create(
            title="test",
            description="test",
            meeting_time=datetime.now() + timedelta(days=10),
        )
        Event.objects.create(
            title="test_2",
            description="test_2",
            meeting_time=datetime.now() + timedelta(days=15),
        )
        cls.event.users.add(cls.user)

    def test_get_user_subscribed_events_by_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_user_subscribed_events(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        events = response.data.get("results")
        for event in events:
            self.assertIn(self.user.username, event.get("users"))
