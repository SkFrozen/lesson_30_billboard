from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from users.models import User

from .models import Event


@shared_task
def sending_event_reminders_next_day() -> None:
    """
    Task checks the available events for tomorrow after 00:00:00
    and sends reminders to users who have subscribed to these event
    """

    events = Event.objects.filter(meeting_time__gt=timezone.now())
    next_day: str = datetime.strftime(datetime.now() + timedelta(days=1), "%d.%m.%Y")

    if not events:
        return

    for event in events:
        if datetime.strftime(event.meeting_time, "%d.%m.%Y") == next_day:
            send_mail(
                "Daily notifications",
                f"Уведомляем вас, что вы согласились посетить {event.title}.\n"
                f"{event.description}\n"
                f"Мероприятие проходит завтра в {event.meeting_time:%H:%M} {event.location}",
                settings.EMAIL_HOST_USER,
                [user.email for user in event.users.all()],
            )


@shared_task
def sending_event_reminders_six_hour(event_id) -> None:
    """
    ???????
    """
    event = Event.objects.get(id=event_id)

    send_mail(
        "Daily notifications",
        f"Уведомляем вас, что вы согласились посетить {event.title}\n"
        f"{event.description}\n"
        f"Мероприяте начинается через 6 часов {event.location}",
        settings.EMAIL_HOST_USER,
        [user.email for user in event.users.all()],
    )


@shared_task
def sending_notification_event_post_save(event_id) -> None:
    event = Event.objects.get(id=event_id)

    send_mail(
        "New event created",
        f"Новое мероприятие:  {event.title}.\n"
        f"{event.description}\n"
        f"Мероприятие проходит {event.meeting_time:%d.%m.%Y %H:%M}  {event.location}",
        settings.EMAIL_HOST_USER,
        [user.email for user in User.objects.all() if user.notify],
    )
