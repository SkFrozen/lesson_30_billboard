from datetime import timedelta

from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Event
from .permission import IsOwner
from .serializers import EventSerializer, EventSubscribeSerializer


class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(meeting_time__gt=timezone.now())
    serializer_class = EventSerializer


class EventSubscribeAPIView(generics.UpdateAPIView):
    queryset = Event.objects.filter(
        meeting_time__gt=timezone.now() + timedelta(hours=2)
    )

    serializer_class = EventSubscribeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"


class EventUserAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsOwner,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(users=request.user)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
