from datetime import datetime

from django import setup
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Event


class TestReadCreateEvent(TestCase):
    """
    Testing user permission to  read and create events.

    """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse("event_list_create")
        cls.event_1 = Event.objects.create(
            title="test_title",
            description="test_description",
            meeting_time="2022-01-01 12:00:00",
        )
        cls.event_2 = Event.objects.create(
            title="test_title_2",
            description="test_description_2",
            meeting_time="2024-11-21 12:00:00",
        )

    def test_can_read_event_list_by_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, response.content)

    def test_can_create_event(self):
        response = self.client.post(
            self.url,
            {
                "title": "Test Event",
                "description": "Test Event Description",
                "meeting_time": "2022-01-01 12:30:00",
            },
        )

        self.assertEqual(response.status_code, 201, response.content)

    def test_get_filtered_queryset_by_date(self):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = self.client.get(self.url)
        events = response.data.get("results")

        for event in events:
            self.assertGreater(event.get("meeting_time"), time)

    def test_paginate_event_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("count", response.data)
        self.assertGreater(len(response.data.get("results")), 0)
