from datetime import timedelta

from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .serializers import EventSerializer, EventSubscribeSerializer


class EventListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(meeting_time__gt=timezone.now())


class EventSubscribeAPIView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSubscribeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"


class EventUserAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Event.objects.filter(users=self.request.user)
