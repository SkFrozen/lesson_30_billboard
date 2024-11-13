from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mass_mail
from django.utils import timezone
from users.models import User

from .models import Event


def send_event_reminder(event: Event, emails: list) -> None:
    """
    The function sends users an email with a reminder about an upcoming event.
    """

    subcject = "Daily notifications"
    message = (
        f"Уведомляем вас, что вы согласились посетить {event.title}.\n"
        f"{event.description}\n"
        f"Начало мероприятия: {event.meeting_time:%#d %B (%A) в %H:%M} {event.location}"
    )
    limit = 10

    for i in range(0, len(emails), limit):
        messages = [
            (subcject, message, settings.EMAIL_HOST_USER, [email])
            for email in emails[i : i + limit]
        ]
        send_mass_mail((messages))


@shared_task
def send_remind_before_event(before_start: int, before_end=1) -> None:
    """
    The task filters upcoming events by time and sends reminders to users

    before_start: the time at which the search begins in hours
    before_end: the time at which the search ends in hours
    """

    now = timezone.now()
    start = timezone.make_aware(
        datetime(now.year, now.month, now.day, now.hour) + timedelta(hours=before_start)
    )
    end = start + timedelta(hours=before_end)

    limit = 10
    start_index = 0
    end_index = limit
    qs = Event.objects.filter(meeting_time__range=(start, end)).prefetch_related(
        "users"
    )[start_index:end_index]

    while qs:
        for event in qs:
            emails = [user.email for user in event.users.all()]

            if emails:
                send_event_reminder(event, emails)

        start_index += limit
        end_index += limit
        qs = Event.objects.filter(meeting_time__range=(start, end)).prefetch_related(
            "users"
        )[start_index:end_index]


@shared_task
def send_notification(event_id: int, emails: list) -> None:
    """
    The task is to send a notification to the user who has the notify is True
    """

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return

    subject = "Новое мероприятие"
    message = (
        f"Новое мероприятие: {event.title}!\n"
        f"{event.description}\n"
        f"Мероприятие проходит {event.meeting_time:%#d %B (%A) в %H:%M} {event.location}\n"
    )
    messages = [
        (subject, message, settings.EMAIL_HOST_USER, [email]) for email in emails
    ]
    send_mass_mail(messages)


@shared_task
def send_notification_event_post_save(event_id) -> None:
    """
    The task is to send a notification when the event is saved
    """

    users = User.objects.filter(notify=True)
    emails = list(users.values_list("email", flat=True))
    limit = 10

    for i in range(0, len(emails), limit):
        send_notification(event_id, emails[i : i + limit])
