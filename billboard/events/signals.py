from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event
from .tasks import sending_notification_event_post_save


@receiver(post_save, sender=Event)
def post_save_event(sender, instance, created, **kwargs):

    if created:
        sending_notification_event_post_save.delay(instance.id)