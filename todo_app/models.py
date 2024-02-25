from django.db import models
from django.contrib.auth.models import AbstractUser


class ToDo(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2000)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# root
    # root
