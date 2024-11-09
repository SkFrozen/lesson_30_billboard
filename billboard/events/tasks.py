from datetime import datetime, timedelta
from tkinter import HORIZONTAL
from tracemalloc import start

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.utils import timezone
from users.models import User

from .models import Event


@shared_task
def sending_event_remind(event_id: int, emails: list) -> None:
    """
    The task is to send the user an email with a reminder of the upcoming event
    """

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return

    if timezone.now() > event.meeting_time:
        return

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
def sending_event_reminders_next_day() -> None:
    """
    The task is to check the available events for tomorrow after 00:00:00
    and send reminders to users who have subscribed to these events
    """

    now = timezone.now()
    tomorrow_start = timezone.make_aware(
        datetime(now.year, now.month, now.day) + timedelta(days=1)
    )
    tomorrow_end = tomorrow_start + timedelta(days=1) - timedelta(seconds=1)
    limit = 10
    start_index = 0
    end_index = limit
    qs = Event.objects.filter(meeting_time__range=(tomorrow_start, tomorrow_end))[
        start_index:end_index
    ]

    while qs:
        for event in qs:
            emails = [user.email for user in event.users.all()]

            if emails:
                sending_event_remind.delay(event.id, emails)

        start_index += limit
        end_index += limit
        qs = Event.objects.filter(meeting_time__range=(tomorrow_start, tomorrow_end))[
            start_index:end_index
        ]


@shared_task
def sending_event_reminders_start_in_6_hours():

    now = timezone.now()
    today_start = timezone.make_aware(
        datetime(now.year, now.month, now.day, now.hour) + timedelta(hours=6)
    )
    today_end = today_start + timedelta(hours=1) - timedelta(seconds=1)
    limit = 10
    start_index = 0
    end_index = limit
    qs = Event.objects.filter(meeting_time__range=(today_start, today_end))[
        start_index:end_index
    ]
    print(f"{today_start} : {today_end} - {qs}")
    while qs:
        for event in qs:
            emails = [user.email for user in event.users.all()]

            if emails:
                sending_event_remind.delay(event.id, emails)

        start_index += limit
        end_index += limit
        qs = Event.objects.filter(meeting_time__range=(today_start, today_end))[
            start_index:end_index
        ]


@shared_task
def sending_notification(event_id: int, emails: list) -> None:
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
def sending_notification_event_post_save(event_id) -> None:
    """
    The task is to send a notification when the event is saved
    """

    users = User.objects.filter(notify=True)
    emails = list(users.values_list("email", flat=True))
    limit = 10

    for i in range(0, len(emails), limit):
        sending_notification(event_id, emails[i : i + limit])
