from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    meeting_time = models.DateTimeField()
    location = models.CharField(max_length=50)
    tags = models.ManyToManyField("Tag", blank=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "events"
        ordering = ["-meeting_time"]


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, primary_key=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tags"
