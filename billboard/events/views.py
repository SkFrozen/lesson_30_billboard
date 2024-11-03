from django.core.cache import cache
from django.utils import timezone
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Event
from .permissions import IsAdminOrReadOnly
from .serializers import EventSerializer, EventSubscribeSerializer


class EventListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, *args, **kwargs):
        page = self.request.query_params.get("page", 1)
        cache_key = f"events_list:{page}"
        cache_timeout = 60
        data = cache.get(cache_key)

        if data is None:
            response = super().get(request, *args, **kwargs)
            data = response.data
            cache.set(cache_key, data, cache_timeout)

        return Response(data)

    def get_queryset(self):
        return Event.objects.filter(meeting_time__gt=timezone.now())


class EventSubscribeAPIView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSubscribeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"


class EventUserAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        page = self.request.query_params.get("page", 1)
        cache_key = f"user_events:{request.user.username}{page}"
        cache_timeout = 60
        data = cache.get(cache_key)

        if data is None:
            response = super().get(request, *args, **kwargs)
            data = response.data
            cache.set(cache_key, data, cache_timeout)

        return Response(data)

    def get_queryset(self):
        return Event.objects.filter(users=self.request.user)
