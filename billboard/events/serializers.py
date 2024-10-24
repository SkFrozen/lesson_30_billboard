from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        many=True, slug_field="username", read_only=True
    )

    class Meta:
        model = Event
        fields = ("title", "meeting_time", "description", "users")


class EventSubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ("users",)

    def create(self, validated_data):
        event = get_object_or_404(
            Event,
            id=self.context["view"].kwargs["id"],
            meeting_time__gt=timezone.now() + timedelta(hours=2),
        )
        event.users.add(self.context["request"].user)
        return event
