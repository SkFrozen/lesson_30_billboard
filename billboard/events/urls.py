from django.urls import path

from . import views

urlpatterns = [
    path("", views.EventListCreateAPIView.as_view(), name="event_list_create"),
    path("<int:id>/", views.EventSubscribeAPIView.as_view(), name="event_subscribe"),
    path("my/", views.EventUserAPIView.as_view(), name="user_events"),
]
