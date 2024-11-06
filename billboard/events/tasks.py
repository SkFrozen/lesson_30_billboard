import time
from datetime import date, datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from users.models import User

from .models import Event


@shared_task
def sending_event_reminders_next_day():
    events = Event.objects.filter(meeting_time__gt=timezone.now())
    next_day: str = datetime.strftime(datetime.now() + timedelta(days=1), "%d.%m.%Y")

    for event in events:
        if datetime.strftime(event.meeting_time, "%d.%m.%Y") == next_day:
            status = send_mail(
                "Daily notifications",
                f"Уведомляем вас, что вы согласились посетить {event.title}.\n"
                f"{event.description}\n"
                f"Мероприятие проходит завтра в {event.meeting_time:%H:%M} {event.location}",
                settings.EMAIL_HOST_USER,
                [user.email for user in event.users.all()],
            )
            print(status)
