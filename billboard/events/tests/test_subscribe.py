from django.test import Client, TestCase
from users.models import User

from ..models import Event


class TestEventSubscribe(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = "/api/v1/events/"
        cls.user = User.objects.create(username="test", password="test123")
        cls.event = Event.objects.create(
            title="test", description="test", meeting_time="2024-10-10 13:20:00"
        )
        cls.event = Event.objects.create(
            title="test2", description="test2", meeting_time="2024-12-10 10:20:00"
        )

    def test_cant_subscribe_event_by_anonymous(self):
        print(User.objects.all())
        response = self.client.get(self.url + "1/")
        self.assertEqual(response.status_code, 401)

    def test_can_subscribe_event_by_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url + "2/")
        self.assertEqual(response.status_code, 201, response.content)

    def test_cant_subscribe_passed_event(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url + "1/")
        self.assertEqual(response.status_code, 404, response.content)
