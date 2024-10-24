from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    email = models.EmailField()

    class Meta:
        db_table = "users"
