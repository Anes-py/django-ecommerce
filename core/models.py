from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    usable_password = models.BooleanField(default=True)
