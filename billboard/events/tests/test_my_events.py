from django.test import Client, TestCase
from django.urls import reverse

from ..models import Event


class TestMyEventList(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse("user_events")
        cls.event = Event.objects.create(
            title="test", description="test", meeting_time="2024-11-13 10:00:00"
        )
